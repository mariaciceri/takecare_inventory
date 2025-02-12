from django.test import TestCase
from django.urls import reverse
from datetime import date
from ordering.models import CustomUser
from ordering.models import Category, Item, Order, OrderItem

class TestOrderingViews(TestCase):

    def setUp(self):
        self.approved_user = CustomUser.objects.create_user(
            username="approvedUser",
            password="approvedUser",
            email="approvedUser@test.com",
            is_approved=True
        )

        self.not_approved_user = CustomUser.objects.create_user(
            username="notApprovedUser",
            password="notApprovedUser",
            email="notApprovedUser@test.com",
            is_approved=False
        )

        self.category = Category.objects.create(
            name="myCategory",
            description="myDescription"
            )

        self.item = Item.objects.create(
            name="Test Item",
            category=self.category,
            expiration_date=date(2025, 12, 31),
            is_critical=True,
            quantity_in_stock=100
            )

        self.order = Order.objects.create(
            user=self.approved_user,
            status=0
            )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            item=self.item,
            quantity=10
            )

    def test_redirect_if_not_authenticated(self):
        """
        Test that the user is redirected to the login page 
        if not authenticated.
        """
        response = self.client.get(reverse("order"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/home/?next=/")

    def test_render_home_page(self):
        """Test that the home page is rendered correctly."""

        self.client.login(username="approvedUser", password="approvedUser")
        response = self.client.get(reverse("order"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ordering/order.html")

    def test_approved_user_correct_content(self):
        """ 
        Test that the correct content is displayed for an approved user.
        """
        self.client.login(username="approvedUser", password="approvedUser")
        response = self.client.get(reverse("order"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, approvedUser")
        self.assertContains(response, "Test Item")

    def test_not_approved_user_correct_content(self):
        """ 
        Test that the correct content is displayed for a not approved user.
        """
        self.client.login(
            username="notApprovedUser", password="notApprovedUser")
        response = self.client.get(reverse("order"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, notApprovedUser")
        self.assertContains(
            response, "To use our page you must register and be approved")
    
    def test_sucessful_add_item_to_session(self):
        """Test that an item is successfully added to the session."""

        self.client.login(username="approvedUser", password="approvedUser")
        response = self.client.post(reverse
            ("add_item_to_session"),
            {"item": self.item.id, "item-quantity": "10"},
        )

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'success': 'Item added to order.',
                'order_items': [{
                    'item_id': str(self.item.id),
                    'name': self.item.name,
                    'quantity': 10
                }]
            }
        )

        self.assertEqual(response.status_code, 200)
        json_response = response.json()

        self.assertIn("order_items", json_response)
        self.assertEqual(len(json_response["order_items"]), 1)
        self.assertEqual(
            json_response["order_items"][0]["item_id"], str(self.item.id))
        self.assertEqual(
            json_response["order_items"][0]["quantity"], 10
        )

    def test_successful_place_an_order(self):
        """Test that an order is successfully placed."""

        self.client.login(username="approvedUser", password="approvedUser")
        
        session = self.client.session
        session["order_items"] = [{
            "item_id": self.item.id,
            "name": self.item.name,
            "quantity": 10
        }]
        session.save()

        response = self.client.post(reverse("create_order"))
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'success': 'Order saved successfully.'
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        """Test that an item is successfully removed from the session."""

        self.client.login(username="approvedUser", password="approvedUser")
        
        session = self.client.session
        session["order_items"] = [{
            "item_id": self.item.id,
            "name": self.item.name,
            "quantity": 10
        }]
        session.save()

        response = self.client.post(reverse(
            "delete_item",
            kwargs={"item_id": str(self.item.id)}
            )
        )

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                "success": "Item removed from order.",
                "order_items": []
            }
        )

        self.assertEqual(response.status_code, 200)
        json_response = response.json()

        self.assertIn("order_items", json_response)
        self.assertEqual(len(json_response["order_items"]), 0)

    def test_update_item_quantity(self):
        """ 
        Test that the quantity of an item is successfully updated or
        if the quantity is greater than the quantity in stock, an error message
        is returned and the quantity's set to the max in stock.
        """
        self.client.login(username="approvedUser", password="approvedUser")

        session = self.client.session
        session["order_items"] = [{
            "item_id": self.item.id,
            "name": self.item.name,
            "quantity": 10
        }]
        session.save()

        response = self.client.post(reverse(
            "update_item_quantity",
            kwargs={"item_id": str(self.item.id)}),
            {"quantity": 5}
        )
        
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                "success": "Item quantity updated.",
                "order_items": [{
                    "item_id": self.item.id,
                    "name": self.item.name,
                    "quantity": 5
                }]
            }
        )

        response = self.client.post(reverse(
            "update_item_quantity",
            kwargs={"item_id": str(self.item.id)}),
            {"quantity": 999}
        )

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                "error": "Insufficient stock.",
                "message": (
                    f"Only {self.item.quantity_in_stock} items available."
                ),
                "max_quantity": self.item.quantity_in_stock
            }
        )

    def test_edit_order(self):
        """Test that an order can be successfully edited."""
        
        self.client.login(username="approvedUser", password="approvedUser")
        
        response = self.client.get(reverse(
            "edit_order",
            kwargs={"order_id": self.order.id})
        )

        session = self.client.session
        session["order_items"] = [{
            "item_id": self.item.id,
            "name": self.item.name,
            "quantity": 10
        }]
        session.save()

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                "success": "Order edited successfully."
            }
        )
