from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NewVisitorTest(StaticLiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(1)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	# page title and header
	def test_check_title(self):
		self.browser.get(self.live_server_url)
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# input box
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

		# insert value
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)

		edith_list_url = self.browser.current_url
		# check redirection to new url
		self.assertRegexpMatches(edith_list_url, '/lists/.+/')

		self.check_for_row_in_list_table('1: Buy peacock feathers')

		# insert second value
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		# check values
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		self.browser.quit()

		# new user
		self.browser = webdriver.Firefox()
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		francis_list_url = self.browser.current_url
		self.assertNotEqual(edith_list_url, francis_list_url)
		self.assertRegexpMatches(francis_list_url, '/lists/.+')
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

	def test_layout_and_styling(self):
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024,768)
		# main.html
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width']/2,
			512,
			delta=5
		)
		# list.html
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width']/2,
			512,
			delta=5
		)
