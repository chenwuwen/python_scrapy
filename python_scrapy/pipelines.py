# -*- coding: utf-8 -*-
# 爬虫pipeline，用于处理提取的结构，比如清洗数据、去重等 ，其内部三个函数
# 第一个open_spider在spider开始的时候执行，在这个函数中我们一般会连接数据库，为数据存储做准备
# process_item函数在捕捉到item的时候执行，一般我们会在这里做数据过滤并且把数据存入数据库
# close_spider在spider结束的时候执行，一般用来断开数据库连接或者做数据收尾工作
# 写好pipeline之后我们需要到settings.py中开启pipeline
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

import pymysql


class PythonScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class NetWorkSchoolPipeline(object):
    mysql_host = '127.0.0.1'
    mysql_port = 3306
    mysql_username = 'root'
    mysql_password = 'root'
    mysql_dbname = 'cpa'
    mysql_cursor = None
    mysql_conn = None

    select_data_dic = {0: 'A', 1: 'B', 2: 'C', 4: 'D', 5: 'E'}

    def open_spider(self, spider):
        print("========建立mysql连接=============")
        self.mysql_conn = pymysql.connect(host=self.mysql_host,
                                          port=self.mysql_port,
                                          user=self.mysql_username,
                                          passwd=self.mysql_password,
                                          db=self.mysql_dbname)
        self.mysql_cursor = self.mysql_conn.cursor()
        pass

    def process_item(self, item, spider):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        choice = 'single'
        if item['choice'] == '多选题':
            choice = 'multiple'
        cpa_repertory = {
            'test_item': item['test_stem'],
            'choice': choice,
            'test_type': item['test_type'],
            'insert_date': now
        }
        cpa_repertory_insert_sql = """ insert into cpa_repertory (test_item,choice,test_type,insert_date)
                                    values (%(test_item)s,%(choice)s,%(test_type)s,%(insert_date)s) """
        self.mysql_cursor.execute(cpa_repertory_insert_sql, cpa_repertory)
        self.mysql_conn.commit()
        # 获取返回的主键
        re_id = self.mysql_cursor.lastrowid
        cpa_option_list = []
        for option, index in enumerate(item['option_data'], 0):
            cpa_option = {
                're_id': re_id,
                'option_data': option,
                'select_data': self.select_data_dic[index]
            }
            cpa_option_list.append(cpa_option)
        cpa_option_insert_sql = """ insert into cpa_option (re_id,option_data,select_data)
                                    values(%(re_id)s,%(option_data)s,%(select_data)s)"""
        self.mysql_cursor.execute(cpa_option_insert_sql)
        self.mysql_conn.commit()

        cpa_solution = {
            're_id': re_id,
            'result': item['result']
        }

        cpa_solution_insert_sql = """ insert into cpa_solution (re_id,result)
                                        values(%(re_id)s,%(result)s,)"""

        self.mysql_cursor.execute(cpa_solution_insert_sql, cpa_solution)
        self.mysql_conn.commit()

    def close_spider(self, spider):
        self.mysql_cursor.close()
        self.mysql_conn.close()
        pass
