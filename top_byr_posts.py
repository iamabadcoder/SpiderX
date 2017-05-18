# -*- coding:utf-8 -*-

import sys
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

reload(sys)
sys.setdefaultencoding('utf8')


def login(driver, home_page_url):
	driver.get(home_page_url)
	try:
		id_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "u_login_id")))
		passwd_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "u_login_passwd")))
		submit_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "u_login_submit")))
		id_element.send_keys(user_name)
		time.sleep(1)
		passwd_element.send_keys(user_pwd)
		time.sleep(1)
		submit_element.click()
		time.sleep(3)
		return True
	except TimeoutException:
		print 'TimeoutException occur when login'
	return False


def top_post(driver, post_url):
	driver.get(post_url)
	try:
		post_content_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "post_content")))
		post_content_element.click()
		time.sleep(1)
		post_content_element.clear()
		post_content_element.send_keys('up')
	except TimeoutException:
		print 'TimeoutException occur when top_post'

	try:
		publish_element = WebDriverWait(driver, 30).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "#post_form > div > input:nth-child(1)")))
		publish_element.click()
		time.sleep(1)
	except TimeoutException:
		print 'TimeoutException occur when top_post'


if __name__ == '__main__':

	user_name = 'lxzcyh'
	user_pwd = ''
	home_page_url = 'https://bbs.byr.cn/#!default'
	post_urls = ['https://bbs.byr.cn/#!article/Jump/post/25367']

	driver = webdriver.Chrome('/Users/caolei/PyWorkSpace/SpiderX/drivers/chromedriver')
	driver.maximize_window()

	if login(driver, home_page_url):
		for post_url in post_urls:
			top_post(driver, post_url)
			time.sleep(10)
