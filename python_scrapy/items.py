# -*- coding: utf-8 -*-
# 爬虫item， 用于定义数据结构
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PythonScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NetWorkSchoolRepertoryItem(scrapy.Item):
    # 题干
    test_stem = scrapy.Field()
    # 题型
    choice = scrapy.Field()
    # 试题类型
    test_type = scrapy.Field()


class NetWorkSchoolOptionsItem(scrapy.Item):
    # 选择答案A,B,C,D
    select_data = scrapy.Field()
    # 答案内容
    option_data = scrapy.Field()
