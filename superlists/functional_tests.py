from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_check_title(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish Test!')



if __name__ == '__main__':
	unittest.main()