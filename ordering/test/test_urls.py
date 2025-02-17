from django.test import TestCase
from django.urls import reverse, resolve
from ordering.views import (
    order, add_item_to_session, create_order, edit_order, delete_item,
    filter_items, order_view, order_items, session_items, update_item_quantity
)


class TestUrls(TestCase):

    def test_order_url_is_resolved(self):
        url = reverse('order')
        self.assertEqual(resolve(url).func, order)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_add_item_url_is_resolved(self):
        url = reverse('add_item_to_session')
        self.assertEqual(resolve(url).func, add_item_to_session)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_create_order_url_is_resolved(self):
        url = reverse('create_order')
        self.assertEqual(resolve(url).func, create_order)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_edit_order_url_is_resolved(self):
        url = reverse('edit_order', args=['1'])
        self.assertEqual(resolve(url).func, edit_order)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_item_url_is_resolved(self):
        url = reverse('delete_item', args=['1'])
        self.assertEqual(resolve(url).func, delete_item)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_filter_item_url_is_resolved(self):
        url = reverse('filter_items', args=['1'])
        self.assertEqual(resolve(url).func, filter_items)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_order_view_url_is_resolved(self):
        url = reverse('order_view')
        self.assertEqual(resolve(url).func, order_view)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_order_items_url_is_resolved(self):
        url = reverse('order_items', args=['1'])
        self.assertEqual(resolve(url).func, order_items)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_session_items_url_is_resolved(self):
        url = reverse('session_items')
        self.assertEqual(resolve(url).func, session_items)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_update_item_urls_is_resolved(self):
        url = reverse('update_item_quantity', args=['1'])
        self.assertEqual(resolve(url).func, update_item_quantity)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
