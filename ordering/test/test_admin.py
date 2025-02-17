import datetime
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from ordering.admin import OrderAdmin, ItemAdmin, CustomUserAdmin
from ordering.models import Order, Item, CustomUser, Category


class TestOrderAdmin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()
        self.admin = OrderAdmin(Order, self.site)
        self.user = CustomUser.objects.create(
            username="testuser",
            email="test@example.com",
            is_approved=True)
        self.order = Order.objects.create(user=self.user, status=0)

    def test_approve_orders(self):
        """Test that approve_orders method works correctly and
        an already approved order can't be processed again"""
        request = self.factory.post("/")
        setattr(request, "session", {})
        setattr(request, "_messages", FallbackStorage(request))

        queryset = Order.objects.filter(id=self.order.id)
        self.admin.approve_orders(request, queryset)

        self.order.refresh_from_db()

        self.assertEqual(self.order.status, 1)

        messages = list(get_messages(request))
        self.assertTrue(any(
            "Order 1 was approved." in msg.message for msg in messages)
            )

        self.admin.approve_orders(request, queryset)
        messages = list(get_messages(request))
        self.assertTrue(any(
            "Order 1 was already processed."
            in msg.message for msg in messages))

        self.admin.reject_orders(request, queryset)
        messages = list(get_messages(request))
        self.assertTrue(any(
            "Order 1 was already processed."
            in msg.message for msg in messages))

    def test_reject_orders(self):
        """Test that reject_orders method works correctly and
        an already rejected order can't be rejected again"""
        request = self.factory.post("/")
        setattr(request, "session", {})
        setattr(request, "_messages", FallbackStorage(request))

        queryset = Order.objects.filter(id=self.order.id)
        self.admin.reject_orders(request, queryset)

        self.order.refresh_from_db()

        self.assertEqual(self.order.status, 2)

        messages = list(get_messages(request))
        self.assertTrue(any(
            "Order 1 was rejected." in msg.message for msg in messages))

        self.admin.reject_orders(request, queryset)
        messages = list(get_messages(request))
        self.assertTrue(any(
            "Order 1 was already processed."
            in msg.message for msg in messages))

        self.admin.approve_orders(request, queryset)
        messages = list(get_messages(request))
        self.assertTrue(any(
            "Order 1 was already processed."
            in msg.message for msg in messages))


class TestItemAdmin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()
        self.admin = ItemAdmin(Item, self.site)
        self.admin_user = CustomUser.objects.create_superuser(
            username="admin", password="password")
        self.client.login(username="admin", password="password")

    def test_date_picker_for_expiration_date(self):
        """Test that date picker is enabled for expiration_date field"""
        response = self.client.get(reverse("admin:ordering_item_add"))
        self.assertContains(response, 'type="date"')
        today = datetime.date.today()
        self.assertContains(
            response, f'min="{today + datetime.timedelta(days=1)}"')

    def test_low_stock_alert(self):
        """Test that low_stock_alert method works correctly"""
        item = Item.objects.create(
            name="Test Item",
            category=Category.objects.create(name="Test Category"),
            quantity_in_stock=99,
            expiration_date="2025-10-10",
            is_critical=True)
        response = self.client.get(reverse('admin:ordering_item_changelist'))
        self.assertContains(response, "Low Stock", html=True)
        item.quantity_in_stock = 100
        self.assertContains(response, "", html=True)

    def test_close_expiration_date(self):
        """Test that close_exp_date method works correctly"""
        item = Item.objects.create(
            name="Test Item",
            category=Category.objects.create(name="Test Category"),
            quantity_in_stock=102,
            expiration_date="2025-03-03",
            is_critical=True)
        response = self.client.get(reverse('admin:ordering_item_changelist'))
        self.assertContains(response, "Close Expiration Date", html=True)

        item.expiration_date = "2025-01-01"
        item.save()
        response = self.client.get(reverse('admin:ordering_item_changelist'))
        self.assertContains(response, "Expired", html=True)

    def test_module_permissions_warnings(self):
        """Test that the module permissions warnings are displayed"""
        category = Category.objects.create(name="Test Category")
        expired_item = Item.objects.create(
            name="Test Item 1",
            category=category,
            quantity_in_stock=102,
            expiration_date="2024-10-12",
            is_critical=False)
        expiring_item = Item.objects.create(
            name="Test Item 2",
            category=category,
            quantity_in_stock=102,
            expiration_date="2025-03-03",
            is_critical=False)
        low_stock_item = Item.objects.create(
            name="Test Item 3",
            category=category,
            quantity_in_stock=55,
            expiration_date="2025-10-12",
            is_critical=False)
        out_stock_item = Item.objects.create(
            name="Test Item 4",
            category=category,
            quantity_in_stock=0,
            expiration_date="2025-10-12",
            is_critical=False)

        response = self.client.get(reverse('admin:index'))

        self.assertIn("admin_warnings", self.client.session)
        warnings = self.client.session["admin_warnings"]
        self.assertEqual(len(warnings), 4)
        self.assertIn("1 item(s)\nare close to expiration!", warnings[0])
        self.assertIn("1 item(s) have expired!", warnings[1])
        self.assertIn("1 item(s) are low in stock!", warnings[2])
        self.assertIn("1 item(s) are out of stock!", warnings[3])


class TestCustomUserAdmin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()
        self.admin = CustomUserAdmin(CustomUser, self.site)
