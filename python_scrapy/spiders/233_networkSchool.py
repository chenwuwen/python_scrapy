# -*- coding: utf-8 -*-
import scrapy
import logging
import sys
import re
import json

# MD5加密用到的包
import hashlib
# BeautifulSoup是Python的一个库，最主要的功能就是从网页爬取我们需要的数据。
# BeautifulSoup将html解析为对象进行处理，全部页面转变为字典或者数组，相对于正则表达式的方式，可以大大简化处理过程。
# BeautifulSoup默认支持Python的标准HTML解析库，但是它也支持一些第三方的解析库： https://blog.csdn.net/kikaylee/article/details/56841789
from bs4 import BeautifulSoup

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


class NetworkSchoolSpider(scrapy.Spider):
    name = '233_networkSchool'
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
        # 把返回的的html保存到文件,方便查找,因为如果html内容太多,控制台会清空部分数据,只在开发时使用,w 模式表示：
        # 如果没有这个文件，就创建一个；如果有，那么就会先把原文件的内容清空再写入新的东西。所以若不想清空原来的内容而是直接在后面追加新的内容，就用'a'这个模式。
        # 关于open()的mode参数：
        # 'r'：读  'w'：写  'a'：追加  'r+' == r+w（可读可写，文件若不存在就报错(IOError)) 'w+' == w+r（可读可写，文件若不存在就创建）
        # 'a+' == a + r（可追加可写，文件若不存在就创建）对应的，如果是二进制文件，就都加一个b就好啦： 'rb'　　'wb'　　'ab'　　'rb+'　　'wb+'　　'ab+'
        # with open('目录.html', 'w+', encoding='utf-8') as data:
        #     data.write(response.text)

        # 创建BeautifulSoup对象 这里我需要找到当前返回的页面的全局变量,这里使用BeautifulSoup来查找[使用Python内置标准库；执行速度快	容错能力较差]
        bs = BeautifulSoup(response.text, 'html.parser')

        # BeautifulSoup 用法: limit参数表示找几个,因为已知要找的全局变量在第四个,所以这里限制找几个
        # chapterClassId = bs.find_all(text="var chapterClassId")
        scripts = bs.find_all('script', limit=4)
        # 找到包含全局变量的script代码块,将其转换成字符串
        script = scripts[3].text
        # 正则表达式：找到“ var chapterClassId= 后面的值”
        reg = re.compile(r"(?<=var chapterClassId=)\d+")
        match = reg.search(script)
        chapterClassId = match.group(0)
        print("查找全局变量结果：%s, 其类型为：%s" % (chapterClassId, type(chapterClassId)))

        baseAjaxPath = "/tiku/exam/extractexam?classId=%s&type=2&mode=1&objectid=%s&examtype=-1&count=0&redo=%s&isContinue=true&isNotLogin=1&fromUrl=%s"

        # 从根部查找class值为czct的td元素下的a元素,取出其中的src属性值  公式  //某元素[@class='CLASS值']
        # 然而当我仔细观察该网站后发现,地址并不在a标签的href属性中,而是动态产生的，以前的 xpath //td[@class='czct']/a/@href
        # for  in response.xpath("//td[@class='czct']/../@data-chapterid").extract():
        # 需要注意的是,当使用xpath选择class属性时,如果元素包含多个class属性,需要将所有属性都添加上,否则查询不到
        tbodys = response.xpath("//table[@class='ui-table ui-table-row']/tbody").extract()
        for index, tbody in enumerate(tbodys):
            if index == 1:
                # 打印出来的是html的内容
                # print(tbody)
                # 如果需要在html字符串中再次使用选择器,则需要将其封装为Selector选择器对象 https://blog.csdn.net/dawnranger/article/details/50037703
                selector = scrapy.Selector(text=tbody)
                # 这里注意要取相对路径,extract_first() 其返回的是列表的第一项,而不是整个列表,
                chapterId = selector.xpath(".//tr/@data-chapterid").extract_first()
                # 需要注意的是这里的td[1] 中的索引表示第一个,也就是说这里的索引是从1开始的,而不是0  text()获取标签里面的值，extract()则是把selector对象变成字符串
                title = selector.xpath(".//tr/td[1]/h2/a/text()").extract()[1]
                iscz = selector.xpath(".//td[@class='czct']/a/@data-iscz").extract_first()
                # print(iscz)
                url = baseAjaxPath % (chapterClassId, chapterId, iscz, self.start_urls[0])
                url = 'http://wx.233.com' + url
                # logging.info("%s的URL: %s" % (title, url))
                # 试题url解析(有时候会发现,request请求并不走回调函数：解决方法https://blog.csdn.net/honglicu123/article/details/75453107/)
                yield scrapy.Request(url, dont_filter=True, callback=self.parse_item_frame)

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    # 先打开登陆页，随后调用登陆方法
    def start_requests(self):
        yield scrapy.Request(self.get_login_url, dont_filter=True, callback=self.login)

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
        logging.info("发起登陆请求")

        yield scrapy.FormRequest.from_response(response,
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

    # 解析试题页，仅仅只是试题页，试题数据是ajax请求的
    def parse_item_frame(self, response):
        logging.info("======解析试题页面开始=========")
        # print(response.text)

        with open('试题库.html', 'w+', encoding='utf-8') as data:
            data.write(response.text)
        logging.info("======解析试题页面结束=========")
        # 返回的页面内存在ajax请求,ajax请求的url也是动态获取的
        bs = BeautifulSoup(response.text, 'html.parser')
        # 获取所有的script脚本
        scripts = bs.find_all('script')
        script = scripts[6].text
        logging.debug(script)
        # 获取全局变量
        redoReg = re.compile((r"(?<=var redo = )\w+"))
        redoMatch = redoReg.search(script)
        redo = redoMatch.group(0)
        postUrl = "/tiku/api/autoexam/" if redo == 'true' else "/tiku/api/exam/"
        postUrl = "http://wx.233.com{}".format(postUrl)
        logging.debug("请求地址：" + postUrl)

        # 获取ajax请求参数url
        urlReg = re.compile("(?<=data: { url: ')[^}']+", re.DOTALL)
        urlMatch = urlReg.search(script)
        url_data = urlMatch.group(0)
        logging.debug("请求携带数据：" + url_data)
        post_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"

        }
        formdata = {
            'url': url_data
        }

        yield [scrapy.FormRequest.from_response(response,
                                                url=postUrl,
                                                formdata=formdata,
                                                method='post',
                                                headers=post_headers,
                                                callback=self.parse_item,
                                                dont_filter=True)]

    # 解析返回的json数据
    def parse_item(self, response):
        logging.debug("获取试题请求URL")
        # 返回的是json数据
        ret = json.load(response.body)
        if ret['s'] == 10006:  # 操作成功
            get_item_url = ret['list']['url']
            # 该请求返回页面,页面内部包含页面md5值,以及下一次ajax请求url
            yield scrapy.Request(get_item_url, callback=self.parse_ajax_item_page)
        else:
            pass

    # 解析试题页,找到下一次ajax url 及参数
    def parse_ajax_item_page(self, response):
        logging.debug("解析试题页,找到下一次ajax url 及参数")

    # 对请求Ajax返回的试题数据, 进行处理
    def parse_ajax_item_json(self, response):
        logging.debug("对请求Ajax返回的试题数据,进行处理")
