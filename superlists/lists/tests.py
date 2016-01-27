from django.test import TestCase
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from .views import home_page
from .models import Item, List


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
		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))


class ItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		my_list = List()
		my_list.save()
		first_item = Item(text="The First list item")
		first_item.list = my_list
		first_item.save()
		second_item = Item(text="Item the second")
		second_item.list = my_list
		second_item.save()

		saved_items = List.objects.first()
		self.assertEqual(saved_items, my_list)
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text,"The First list item")
		self.assertEqual(first_saved_item.list, my_list)
		self.assertEqual(second_saved_item.text,"Item the second")
		self.assertEqual(second_saved_item.list, my_list)


class LiveViewTest(TestCase):
	# GET items
	def test_displays_only_items_for_that_list(self):
		my_list = List.objects.create()
		Item.objects.create(text='item 1', list=my_list)
		Item.objects.create(text='item 2', list=my_list)
		other_list = List.objects.create()
		Item.objects.create(text='other item 1', list=other_list)
		Item.objects.create(text='other item 2', list=other_list)
		response = self.client.get('/lists/%d/' %(my_list.id,))
		self.assertContains(response, 'item 1')
		self.assertNotContains(response, 'other item 2')

	# GET template
	def test_users_list_template(self):
		my_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (my_list.id,))
		self.assertTemplateUsed(response, 'list.html')


class NewItemTest(TestCase):
	def test_can_save_a_POST_request_to_an_existing_list(self):
		first_list = List.objects.create()
		second_list = List.objects.create()
		self.client.post('/lists/%d/add_item' % (first_list.id, ), data={'item_text': 'a new item'})
		self.assertEqual(Item.objects.count(), 1)
		self.assertEqual(Item.objects.first().text, 'a new item')
		self.assertEqual(Item.objects.first().list, first_list)

	def test_redirects_to_list_view(self):
		first_list = List.objects.create()
		response = self.client.post('/lists/%d/add_item' % (first_list.id, ), data={'item_text': 'a new item'})
		self.assertRedirects(response, '/lists/%d/' % (first_list.id,))

	def test_passes_correct_list_to_template(self):
		first_list = List.objects.create()
		second_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (first_list.id, ))
		self.assertEqual(response.context['list'], first_list)
