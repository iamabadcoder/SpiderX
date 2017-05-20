# -*- coding:utf-8 -*-

import sys
import time
import linecache
import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium.webdriver.support import expected_conditions as EC

reload(sys)
sys.setdefaultencoding('utf8')


def login(driver, home_page_url):
    login_flag = False
    id_element = None
    passwd_element = None
    submit_element = None
    try:
        driver.get(home_page_url)
        id_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "u_login_id")))
        passwd_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "u_login_passwd")))
        submit_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "u_login_submit")))
        login_flag = True
    except TimeoutException:
        print 'TimeoutException occur when WebDriverWait in login'
        driver.get(home_page_url)
    if login_flag is False:
        try:
            id_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "u_login_id")))
            passwd_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "u_login_passwd")))
            submit_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "u_login_submit")))
        except TimeoutException:
            print 'TimeoutException occur when WebDriverWait in login'
    else:
        # id_element.clear()
        id_element.send_keys(conf.get("beiyouren", "name"))
        time.sleep(1)
        # passwd_element.clear()
        passwd_element.send_keys(conf.get("beiyouren", "name"))
        time.sleep(1)
        submit_element.click()
        time.sleep(3)
        return True
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


def login_and_top():
    post_url_count = len(open(file_shuimu_post_urls, "rU").readlines()) + 1
    for i_line in range(1, post_url_count):
        post_url = linecache.getline(file_shuimu_post_urls, i_line)
        if post_url is None or post_url.strip() == '':
            continue
        print post_url
        top_post(driver, post_url)
        time.sleep(interval_of_top_post)


if __name__ == '__main__':
    conf = ConfigParser.ConfigParser()
    conf.read('account.conf')
    home_page_url = 'https://bbs.byr.cn/#!default'
    file_shuimu_post_urls = './posts_tool/beiyouren_post_urls.txt'
    interval_of_top_post = 10  # 循环顶帖的时间间隔
    cycle_time = 300  # 程序运行周期

    driver = webdriver.Chrome('./drivers/chromedriver')
    driver.maximize_window()
    login(driver, home_page_url)

    sched = BlockingScheduler()
    sched.add_job(login_and_top, 'interval', seconds=cycle_time)
    try:
        sched.start()
    except Exception:
        print 'clear job'
        sched.remove_all_jobs()
