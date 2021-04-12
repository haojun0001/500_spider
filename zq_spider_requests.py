import random
import time
import requests
import functools
import json
import os
import pickle
from bs4 import BeautifulSoup
import xlrd
import xlwt
from xlutils.copy import copy
from lxml import etree
from logger import logger
from config import global_config
from exception import SKException
import js2xml


class ZqSpider(object):
    def __init__(self):
        self.in_file_path = global_config.getRaw('config', 'in_file_path')
        self.out_file_path = global_config.getRaw('config', 'out_file_path')
        self.spider_url = global_config.getRaw('config', 'spider_url')
        self.user_agent = global_config.getRaw('config', 'DEFAULT_USER_AGENT')

    def get_duiju(self):
        headers = {
            'User-Agent': self.user_agent,
        }
        logger.info('开始爬取:' + self.spider_url)
        resp = requests.get(url=self.spider_url, headers=headers)
        resp.encoding = 'GBK'
        resp.encoding = 'utf-8'

        logger.info('打开模板文件:' + self.in_file_path)
        rb = xlrd.open_workbook(self.in_file_path,formatting_info=True)
        wb = copy(rb)
        sheet = wb.get_sheet(rb.nsheets - 1)

        logger.info('开始解析联赛积分排名')
        soup = BeautifulSoup(resp.text,'lxml')
        table_first = soup.select('#porlet_5 > div > table > tbody > tr:nth-child(1) > td:nth-child(1) > table')

        trs = table_first[0].find_all('tr')
        i = 0
        cols = 0
        rows = 3
        first_match_name = ""
        for tr in trs:#遍历后续节点
            if i == 0:
                first_match_name = tr.find_all('b')[0].text
                logger.info('开始解析' + first_match_name + '全场')
                sheet.write(rows,cols,tr.find_all('b')[0].text)
                rows = rows + 1
            else:
                cols = 0
                for td in tr.find_all('td'):
                   sheet.write(rows,cols,td.text)
                   cols = cols + 1
                rows = rows + 1
            i = i + 1
        

        table_second = soup.select('#porlet_5 > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > table')
        trs = table_second[0].find_all('tr')
        i = 0
        cols = 11
        rows = 3
        second_match_name = ""
        for tr in trs:#遍历后续节点
            if i == 0:
                second_match_name = tr.find_all('b')[0].text
                logger.info('开始解析' + second_match_name + '全场')
                sheet.write(rows,cols,tr.find_all('b')[0].text)
                rows = rows + 1
            else:
                cols = 11
                for td in tr.find_all('td'):
                   sheet.write(rows,cols,td.text)
                   cols = cols + 1
                rows = rows + 1
            i = i + 1
        
        ban_rows = rows
        logger.info('开始解析' + first_match_name + '半场')
        table_third = soup.select('#porlet_5 > div > table > tbody > tr:nth-child(2) > td:nth-child(1) > table')
        trs = table_third[0].find_all('tr')
        cols = 0
        for tr in trs:#遍历后续节点
            cols = 0
            for td in tr.find_all('td'):
                sheet.write(rows,cols,td.text)
                cols = cols + 1
            rows = rows + 1

        logger.info('开始解析' + second_match_name + '半场')
        table_fourth = soup.select('#porlet_5 > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > table')
        trs = table_fourth[0].find_all('tr')
        cols = 11
        rows = ban_rows
        for tr in trs:#遍历后续节点
            cols = 11
            for td in tr.find_all('td'):
                sheet.write(rows,cols,td.text)
                cols = cols + 1
            rows = rows + 1


        wb.save(self.out_file_path)

        soup = BeautifulSoup(r.text, 'html.parser')
        src = soup.select('#webmain script')[0].string
        # print('---------')
        # print(src)
        src_element = js2xml.parse(src, encoding='utf-8', debug=False)
        # print('---------')
        print(src_element)
        src_tree = js2xml.pretty_print(src_element)
        print('---------')
        print(src_tree)
        print('---------')
        number = src_element.xpath("//program/var[@name='v_data']")


        logger.info('爬取完成:' + self.out_file_path)


