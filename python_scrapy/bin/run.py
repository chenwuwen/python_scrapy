"""
    这个函数跟main函数的效果是一样的,只不过这个是调用scrapy内置的命令行而已,而mian函数则是使用python内置的命令行相关的模块
"""

from scrapy.cmdline import execute

# cmdline定时执行的话，只会执行一次就退出,需要将其改成命令行的方式才可以实现定时执行,即main.py
if __name__ == '__main__':
    execute("scrapy crawl 233_networkSchool".split())
    # 有多个爬虫的话,依次往下写就可以,只需要更改爬虫名称即可
