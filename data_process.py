# -*- coding:utf-8 -*-

import sys
import time
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


if __name__ == '__main__':

	file_product_details = 'product_details.txt'
	file_product_final = 'product_final.txt'
	# 理财产品详情抽取
	for i in range(1, len(open(file_product_details, "rU").readlines()) + 1):
		print 'line i=' + str(i)
		line = linecache.getline(file_product_details, i)
		if '折合' in line:
			next_line = linecache.getline(file_product_details, i + 1).strip()
			next_next_line = linecache.getline(file_product_details, i + 2).strip()
			new_line = line.replace('折合', '').strip() + '\t' + next_line + '\t' + next_next_line.replace('每月等本等息',
																										 '').strip() + '\n'
			write2file(file_product_final, new_line)
		else:
			write2file(file_product_final, line)
