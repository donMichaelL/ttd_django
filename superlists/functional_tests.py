from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(1)

	def tearDown(self):
		self.browser.quit()

	# page title and header
	def test_check_title(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# input box 
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

		# insert value
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)

		# table
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_element_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1:Buy peacock feathers' for row in rows), 
			'New to-do item did not appear in table')
		#self.fail('Finish Test!')



if __name__ == '__main__':
	unittest.main()