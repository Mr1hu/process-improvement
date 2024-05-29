from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitortTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
          start_time = time.time()
          while True:
              try:
                  table= self.browser.find_element(By.ID, 'id_list_table')
                  rows = table.find_elements(By.TAG_NAME,'tr')
                  self.assertIn(row_text, [row.text for row in rows])
                  return
              except (AssertionError, WebDriverException) as e:
                  if time.time() - start_time > MAX_WAIT:
                      raise e
                  time.sleep(0.5)
                      

    def test_can_start_a_list_and_retrieve_it_later(self):

        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element(By.ID,'id_new_item') #(1)
        self.assertEqual(
              inputbox.get_attribute('placeholder'),
              'Enter a to-do item'
        )

        inputbox.send_keys('Buy flowers') #(2)

        inputbox.send_keys(Keys.ENTER) #(3)
        self.check_for_row_in_list_table('1: Buy flowers')

        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('give a gift to list')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy flowers')
        self.check_for_row_in_list_table('2: give a gift to list')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy flowers')

        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Chrome()


        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertNotIn('BGive a gift to List', page_text)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        wangwu_list_url = self.browser.current_url
        self.assertRegex(wangwu_list_url, '/lists/.+')
        self.assertNotEqual(wangwu_list_url, zhangsan_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertIn('Buy milk',page_text)

        self.fail('Finish the test!')
