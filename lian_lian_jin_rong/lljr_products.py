# -*- coding:utf-8 -*-

import sys
import time
import linecache
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def next_page(driver):
	try:
		next_page_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nextPage')))
		next_page_element.click()
		return True
	except TimeoutException:
		print 'TimeoutException occur when next_page'
		return False


def loop_licai_products(driver):
	product_hrefs = []
	product_names = []
	c_blue_elements = driver.find_elements_by_class_name('c_blue')
	for c_blue_ele in c_blue_elements:
		if 'a' in c_blue_ele.tag_name:
			product_hrefs.append(c_blue_ele.get_attribute('href'))
			product_names.append(c_blue_ele.text)
	for i in range(len(product_hrefs)):
		driver.get(product_hrefs[i])
		annual_percentage_rate = ''
		project_duration = ''
		project_scale = ''
		time_for_sale = ''
		sell_out_duration = ''
		buyer_number = ''
		buyer_money = ''
		buy_time = ''
		time.sleep(4)
		try:
			pb20_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'pb20')))
			for ele in pb20_element.find_elements_by_tag_name('li'):
				if '率' in ele.text:
					annual_percentage_rate = ele.text.replace('年利率', '').replace('一次性还本付息', '').strip()
				elif '期限' in ele.text:
					project_duration = ele.text.replace('项目期限', '').strip()
				elif '规模' in ele.text:
					project_scale = ele.text.replace('项目规模', '').strip()

			time_for_sale = driver.find_element_by_class_name('up_time').text.replace('开售时间 : ', '').strip()
			time_for_sale = time_for_sale.replace('市场有风险，投资需谨慎', '').strip()
			full_time_text = driver.find_element_by_class_name('full_time').text.strip()
			sell_out_duration = full_time_text.split('投标笔数：')[0].replace('项目售罄历时', '').strip().replace('\n', '')


		# write2file(file_result, content)

		except TimeoutException:
			print 'TimeoutException occur when loop_licai_products'


def extract_product_links(driver):
	c_blue_elements = driver.find_elements_by_class_name('c_blue')
	for c_blue_ele in c_blue_elements:
		if 'a' in c_blue_ele.tag_name:
			write2file(file_product_links, c_blue_ele.get_attribute('href') + '\t' + c_blue_ele.text + '\n')


def extract_house_info(house_info, type):
	if type == 1:
		fields = house_info.split('婚姻：')
		marriage = fields[1]
		sex = fields[0].split('性别：')[1]
		name = fields[0].split('性别：')[0].replace('姓名：', '').replace('已验证', '')
		return name, sex, marriage
	elif type == 2:
		fields = house_info.split('产权性质：')
		property_right = fields[1]
		value = fields[0].split('市场价值：')[1]
		area = fields[0].split('市场价值：')[0].split('建筑面积：')[1]
		locate = fields[0].split('市场价值：')[0].split('建筑面积：')[0].replace('所处位置：', '')
		return locate, area, value, property_right


def extract_product_detail(driver, product_link, product_name):
	driver.get(product_link)
	try:
		time.sleep(1)

		full_time_ele = driver.find_element_by_class_name('full_time')
		if '统计中' in full_time_ele.text:
			time.sleep(2)
			full_time_ele = driver.find_element_by_class_name('full_time')
			if '统计中' in full_time_ele.text:
				time.sleep(3)
		sell_out_duration = full_time_ele.text.split('投标笔数：')[0].replace('项目售罄历时：', '').strip()
		bid_count = full_time_ele.text.split('投标笔数：')[1].replace('笔', '').strip()

		pb20_element = driver.find_element_by_class_name('pb20')
		for li_ele in pb20_element.find_elements_by_tag_name('li'):
			if '率' in li_ele.text:
				annual_percentage_rate = li_ele.text.replace('年利率', '').replace('一次性还本付息', '').strip()
			elif '期限' in li_ele.text:
				project_duration = li_ele.text.replace('项目期限', '').strip()
			elif '规模' in li_ele.text:
				project_scale = li_ele.text.replace('项目规模', '').strip()

		up_time_ele = driver.find_element_by_class_name('up_time')
		time_for_sale = up_time_ele.text.replace('开售时间 : ', '').replace('市场有风险，投资需谨慎', '').strip()

		# house_info_elements = driver.find_elements_by_class_name('houseInfo')
		# for house_info_ele in house_info_elements:
		# 	if 'h_bc' in house_info_ele.get_attribute('class'):
		# 		name, sex, marriage = extract_house_info(house_info_ele.text.repalce('借款人信息', ''), 1)
		# 		print name, sex, marriage
		# 	else:
		# 		locate, area, value, property_right = extract_house_info(house_info_ele.text.repalce('房产信息', ''), 2)
		# 		print locate, area, value, property_right

		full_list_element = driver.find_element_by_class_name('full_list')
		tbody_element = full_list_element.find_element_by_tag_name('tbody')
		tr_elements = tbody_element.find_elements_by_tag_name('tr')
		for tr_ele in tr_elements:
			for td in tr_ele.find_elements_by_tag_name('td'):
				if '****' in td.get_attribute("innerHTML"):
					buyer_number = td.get_attribute("innerHTML").strip()
				elif ':' in td.get_attribute("innerHTML"):
					buy_time = td.get_attribute("innerHTML").strip()
				else:
					buyer_money = td.get_attribute("innerHTML").strip()
			content = product_name.strip() + '\t' + annual_percentage_rate.strip() + '\t' + project_duration.strip() + '\t'
			content = content + project_scale.strip() + '\t' + time_for_sale.strip() + '\t' + sell_out_duration.strip() + '\t'
			content = content + buyer_number.strip() + '\t' + buyer_money.strip() + '\t' + buy_time.strip() + '\n'
			write2file(file_product_details, content)

	except Exception:
		print 'Exception occur when extract_product_detail' + Exception.message


if __name__ == '__main__':
	home_url = 'https://www.lljr.com/licai'
	file_product_links = 'product_links.txt'
	file_product_details = 'product_details.txt'
	chromedriver = webdriver.Chrome('/Users/caolei/PyWorkSpace/SpiderX/drivers/chromedriver')
	chromedriver.maximize_window()

	# 理财产品链接抽取
	# chromedriver.get(home_url)
	# for page_index in range(287):
	# 	print 'page num:' + str(page_index)
	# 	if page_index > 0:
	# 		next_page(chromedriver)
	# 		time.sleep(2)
	# 	extract_product_links(chromedriver)

	# 理财产品详情抽取
	for i in range(1, len(open(file_product_links, "rU").readlines()) + 1):
		print 'line i=' + str(i)
		line = linecache.getline(file_product_links, i)
		line_split_fields = line.split('\t')
		extract_product_detail(chromedriver, line_split_fields[0], line_split_fields[1])
