from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	# page title and header
	def test_check_title(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		#self.fail('Finish Test!')



if __name__ == '__main__':
	unittest.main()