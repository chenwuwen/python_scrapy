# -*- coding: utf-8 -*-
import scrapy
import logging
import sys
# Scrapy中用作登录使用的一个包
from scrapy import FormRequest
# MD5加密用到的包
import hashlib

logging.basicConfig(level=logging.INFO,  # 设置告警级别为INFO
                    # 自定义打印的格式
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    # 将日志输出到指定的文件中
                    # filename="yinzhengjie.txt",
                    # # 以追加的方式将日志写入文件中，w是以覆盖写的方式哟
                    # filemode="a",
                    handlers=[logging.StreamHandler(sys.stdout)]
                    )


class CpaSpider(scrapy.Spider):
    name = 'cpa'
    # 233网校登陆名,密码 nncf3dot@4059.com  123456
    allowed_domains = ['wx.233.com/']
    start_urls = ['http://wx.233.com/tiku/chapter/48']
    get_login_url = 'http://passport.233.com/login/'
    post_login_url = 'http://passport.233.com/api/singin'

    def parse(self, response):
        # 返回的response是支持Xpath的,直接使用Xpath来提取数据就行啦,Xpath语法：http://www.w3school.com.cn/xpath/xpath_syntax.asp
        # 简单获取XPath的方法是,使用谷歌浏览器,打开控制台工具,选择需要的Dom元素,右键Copy -> Copy Xpath
        # 你会得到这样的内容：
        # // *[ @ id =”post_content”] / p[1]
        # 意思是：在根节点下面的有一个id为post_content的标签里面的第一个p标签（p[1]）
        # 如果你需要提取的是这个标签的文本你需要在后面加点东西变成下面这样：
        # // *[ @ id =”post_content”] / p[1] / text()
        # 后面加上text()标签就是提取文本
        # 如果要提取标签里面的属性就把text()换成 @ 属性比如：//*[@id=”post_content”]/p[1]/@src
        # 注意XPath提取出来的默认是List。
        # response.xpath(‘你Copy的XPath’).extract()[‘要取第几个值’]

        # logging.info(response.text)
        for chapter_url in response.xpath("//[@class='czct']/a/@src"):
            logging.info("第几章节的URL: " + chapter_url)

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    # 先打开登陆页，随后调用登陆方法
    def start_requests(self):
        yield scrapy.Request(self.get_login_url, callback=self.login)

    # 登陆
    def login(self, response):
        # 需要注意的是请求参数只能是str类型的,否则报错:TypeError: to_bytes must receive a unicode, str or bytes object, got int
        # 该网站是将密码加密过后再进行传输的,经过判断使用的是MD5加密,所以这里我也需要加密密码
        formdata = {
            'account': 'nncf3dot@4059.com',
            'password': hashlib.md5('123456'.encode('utf-8')).hexdigest(),
            'remember': 'true'
        }
        logging.info("加密后的密码：" + hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # 请求头参数,可根据浏览器控制台的实际请求头参数
        post_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"

        }
        print("发起登陆请求")

        yield FormRequest.from_response(response,
                                        url=self.post_login_url,
                                        # formdata 的参数必须是字符串
                                        formdata=formdata,
                                        method='post',
                                        # Scrapy通过使用cookiejar Request meta key来支持单spider追踪多cookie session
                                        # meta={'cookiejar': response.meta['cookiejar']},
                                        headers=post_headers,
                                        # 请求成功回调函数
                                        callback=self.parse_login_success,
                                        # 请求失败回调函数
                                        errback=self.parse_login_error,
                                        # 如果需要多次提交表单，且url一样，那么就必须加此参数dont_filter，防止被当成重复网页过滤掉了
                                        dont_filter=True
                                        )

    # 解析登陆返回页面
    def parse_login_success(self, response):
        logging.info("登陆请求成功后的解析页面")
        logging.info("======================================")
        logging.info(response.text)
        # logging.info(response.)
        logging.info("======================================")
        if '操作成功' in response.text:
            logging.info('============登陆成功！===============')
            # 登陆成功开始调用父类的start_requests方法,即开始进行爬取
            yield from super().start_requests()
        else:
            logging.info('==========登陆失败=============')

    # 请求失败
    def parse_login_error(self, response):
        logging.info("请求失败")
