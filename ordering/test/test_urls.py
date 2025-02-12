from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ordering.views import (
    order, add_item_to_session, create_order, edit_order, delete_item,
    filter_items, order_view, order_items, session_items, update_item_quantity
)


class TestUrls(SimpleTestCase):

    def test_order_urls_is_resolves(self):
        url = reverse('order')
        self.assertEqual(resolve(url).func, order)

    def test_order_urls_is_resolves(self):
        url = reverse('add_item_to_session')
        self.assertEqual(resolve(url).func, add_item_to_session)

    def test_order_urls_is_resolves(self):
        url = reverse('create_order')
        self.assertEqual(resolve(url).func, create_order)

    def test_order_urls_is_resolves(self):
        url = reverse('edit_order', args=['1'])
        self.assertEqual(resolve(url).func, edit_order)

    def test_order_urls_is_resolves(self):
        url = reverse('delete_item', args=['1'])
        self.assertEqual(resolve(url).func, delete_item)

    def test_order_urls_is_resolves(self):
        url = reverse('filter_items', args=['testing-category'])
        self.assertEqual(resolve(url).func, filter_items)

    def test_order_urls_is_resolves(self):
        url = reverse('order_view')
        self.assertEqual(resolve(url).func, order_view)

    def test_order_urls_is_resolves(self):
        url = reverse('order_items', args=['1'])
        self.assertEqual(resolve(url).func, order_items)

    def test_order_urls_is_resolves(self):
        url = reverse('session_items')
        self.assertEqual(resolve(url).func, session_items)

    def test_order_urls_is_resolves(self):
        url = reverse('update_item_quantity', args=['1'])
        self.assertEqual(resolve(url).func, update_item_quantity)
