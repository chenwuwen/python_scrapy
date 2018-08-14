"""
    该文件是爬虫运行主函数,默认在本地执行爬虫需要使用命令行：scrapy crawl 爬虫名
    所以我写一个函数,通过Python的命令行工具[subprocess]来代为执行爬虫
    https://www.cnblogs.com/yyds/p/7288916.html
    https://segmentfault.com/a/1190000009176351

"""
import datetime
import subprocess
import os, sys, time, sched

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

# 关于爬虫任务的定时执行有两种方式,一种是代码实现,而是 在操作系统中实现,如Liunx中CronTab
# 代码方式实现
# 1.最简单的方法：直接使用Time类
# if __name__ == '__main__':
#     while True:
#         time.sleep(86400)  # 每隔一天运行一次 24*60*60=86400s
#         print("========启动爬虫=========")
#         start_time = datetime.datetime.now().second
#         subprocess.call('scrapy crawl %s' % (spider_name))
#         end_time = datetime.datetime.now().second
#         print("爬取结束,总计用时：%d秒" % (end_time - start_time))

# 2.使用标准库的sched模块
# 初始化sched模块的scheduler类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
# schedule = sched.scheduler(time.time, time.sleep)


# 被周期性调度触发的函数
# def func():
#     print("========启动爬虫=========")
#     start_time = datetime.datetime.now().second
#     subprocess.call('scrapy crawl %s' % (spider_name))
#     end_time = datetime.datetime.now().second
#     print("爬取结束,总计用时：%d秒" % (end_time - start_time))
#
#
# def perform1(inc):
#     schedule.enter(inc, 0, perform1, (inc,))
#     # 需要周期执行的函数
#     func()
#
#
# def main():
#     schedule.enter(0, 0, perform1, (86400,))
#
#
# if __name__ == '__main__':
#     main()
#     schedule.run()


# 操作系统方式定时执行爬虫任务 ：https://blog.csdn.net/qq_21768483/article/details/78725481