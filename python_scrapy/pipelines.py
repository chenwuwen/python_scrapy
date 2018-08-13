# -*- coding: utf-8 -*-
# 爬虫pipeline，用于处理提取的结构，比如清洗数据、去重等 ，其内部三个函数
# 第一个open_spider在spider开始的时候执行，在这个函数中我们一般会连接数据库，为数据存储做准备
# process_item函数在捕捉到item的时候执行，一般我们会在这里做数据过滤并且把数据存入数据库
# close_spider在spider结束的时候执行，一般用来断开数据库连接或者做数据收尾工作
# 写好pipeline之后我们需要到settings.py中开启pipeline
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime, re

import pymysql

log_name = 'error.log'


class PythonScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class NetWorkSchoolPipeline(object):
    mysql_host = '115.47.147.131'
    mysql_port = 3306
    mysql_username = 'root'
    mysql_password = 'ruifight2018'
    mysql_dbname = 'cpa'
    mysql_cursor = None
    mysql_conn = None

    select_data_dic = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

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
        print("===========进入pipelines中process_item方法,执行数据库操作===========")

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 数据清洗
        test_stem = item['test_stem']
        if '&emsp;' in test_stem:
            test_stem = test_stem.replace('&emsp;', ' ')

        choice = 'single'
        if item['choice'] == '多选题':
            choice = 'multiple'

        cpa_repertory = {
            'test_stem': test_stem,
            'choice': choice,
            'test_type': item['test_type'],
            'insert_date': now
        }
        cpa_repertory_insert_sql = """ insert into cpa_repertory (test_stem,choice,test_type,insert_date)
                                    values (%(test_stem)s,%(choice)s,%(test_type)s,%(insert_date)s) """
        try:
            self.mysql_cursor.execute(cpa_repertory_insert_sql, cpa_repertory)
            self.mysql_conn.commit()
        except Exception as e:
            with open(log_name, 'a+', encoding='utf-8') as log:
                content = []
                content.append("时间：")
                content.append(now)
                content.append("出错SQL：")
                content.append(cpa_repertory_insert_sql % (cpa_repertory))
                content.append("报错内容：")
                content.append(e.__str__())
                content.append("\n")
                log.write("\t".join(content))
        else:
            print("====插入试题表成功=========")

        # 获取返回的主键
        re_id = self.mysql_cursor.lastrowid
        cpa_option_list = []
        # 去掉字符串中的html标签
        reg = re.compile(r'<[^>]+>', re.S)
        for index, option in enumerate(item['option_data'], 0):
            cpa_option = {
                're_id': re_id,
                'option_data': reg.sub('', option),
                'select_data': self.select_data_dic[index]
            }
            cpa_option_list.append(cpa_option)
        cpa_option_insert_sql = """ insert into cpa_option (re_id,option_data,select_data)
                                    values(%(re_id)s,%(option_data)s,%(select_data)s)"""
        try:
            # 需要注意的是批量插入需要使用executemany方法
            self.mysql_cursor.executemany(cpa_option_insert_sql, cpa_option_list)
            self.mysql_conn.commit()
        except Exception as e:
            with open(log_name, 'a+', encoding='utf-8') as log:
                content = []
                content.append("时间：")
                content.append(now)
                content.append("出错SQL：")
                content.append(cpa_option_insert_sql % (cpa_option_list))
                content.append("报错内容：")
                content.append(e.__str__())
                content.append("\n")
                log.write("\t".join(content))
        else:
            print("====插入试题选项表成功=========")

        cpa_solution = {
            're_id': re_id,
            'result': item['result']
        }

        cpa_solution_insert_sql = """ insert into cpa_solution (re_id,result)
                                        values(%(re_id)s,%(result)s)"""
        try:
            self.mysql_cursor.execute(cpa_solution_insert_sql, cpa_solution)
            self.mysql_conn.commit()
        except Exception as e:
            with open(log_name, 'a+', encoding='utf-8') as log:
                content = []
                content.append("时间：")
                content.append(now)
                content.append("出错SQL：")
                content.append(cpa_solution_insert_sql % (cpa_solution))
                content.append("报错内容：")
                content.append(e.__str__())
                content.append("\n")
                log.write("\t".join(content))
        else:
            print("====插入试题答案表成功=========")

    def close_spider(self, spider):
        self.mysql_cursor.close()
        self.mysql_conn.close()
        pass
