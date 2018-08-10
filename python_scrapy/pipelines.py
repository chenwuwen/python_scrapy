# -*- coding: utf-8 -*-
# 爬虫pipeline，用于处理提取的结构，比如清洗数据、去重等
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class PythonScrapyPipeline(object):
    def process_item(self, item, spider):
        return item
