from django.test import TestCase
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from .views import home_page
from .models import Item


class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html', request=request)
		self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_displays_all_list_items(self):
		Item.objects.create(text='item 1')
		Item.objects.create(text='item 2')
		request = HttpRequest()
		response = home_page(request)
		self.assertIn('item 1', response.content.decode())
		self.assertIn('item 2', response.content.decode())

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		response = home_page(request)

		self.assertEqual(Item.objects.count(), 1)
		first_item = Item.objects.first()
		self.assertEqual('A new list item', first_item.text)
		# expected_html = render_to_string('home.html',
		# {'new_item_text': 'A new list item'}, request=request)
		# self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_redirects_after_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		response = home_page(request)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/lists/the-only-list')

	def test_home_page_only_saves_items_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
	def test_saveing_and_retrieving_items(self):
		first_item = Item(text="The First list item")
		first_item.save()
		second_item = Item(text="Item the second")
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text,"The First list item")
		self.assertEqual(second_saved_item.text,"Item the second")
