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
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')


class NewListTest(TestCase):
	# POST SAVE
	def test_saving_a_POST_request(self):
		self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
	# POST REDIRECT
	def test_redirects_after_POST(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertRedirects(response, '/lists/the-only-list/')


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


class LiveViewTest(TestCase):
	# GET items
	def test_displays_all_items(self):
		Item.objects.create(text='item 1')
		Item.objects.create(text='item 2')
		response = self.client.get('/lists/the-only-list/')
		self.assertContains(response, 'item 1')
		self.assertContains(response, 'item 2')

	# GET template
	def test_users_list_template(self):
		response = self.client.get('/lists/the-only-list/')
		self.assertTemplateUsed(response, 'list.html')
