"""
    该文件是爬虫运行主函数,默认在本地执行爬虫需要使用命令行：scrapy crawl 爬虫名
    所以我写一个函数,通过Python的命令行工具[subprocess]来代为执行爬虫
    https://www.cnblogs.com/yyds/p/7288916.html
    https://segmentfault.com/a/1190000009176351

"""
import datetime
import subprocess
import os, sys

print("当前文件真实路径：%s" % (os.path.realpath(__file__)))
print("当前文件绝对路径：%s" % (os.path.abspath(__file__)))
print("当前文件所在文件夹路径：%s" % (os.path.dirname(os.path.realpath(__file__))))
print("当前文件所在文件夹路径：%s" % (os.path.split(os.path.realpath(__file__))[0]))
print("当前当前工作目录为：%s" % (os.getcwd()))
print("被执行脚本所在目录：%s" % (sys.path[0]))
print("被执行脚本所在目录：%s" % (sys.argv[0]))
# 修改当前工作目录
# os.chdir("D:\\")
# print("修改后的工作目录：%s" % (os.getcwd()))

spider_name = '233_networkSchool'

# 关于命令行的执行,只要在scrapy工程下的目录内执行命令即可,不必需是工程根目录下执行
if __name__ == '__main__':
    print("========启动爬虫=========")
    # second获取秒 minute 获取分 microsecond获取毫秒
    start_time = datetime.datetime.now().second
    subprocess.call('scrapy crawl %s' % (spider_name))
    end_time = datetime.datetime.now().second
    print("爬取结束,总计用时：%d秒" % (end_time - start_time))
