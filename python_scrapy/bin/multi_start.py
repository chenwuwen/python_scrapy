from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
    # 通过get_project_settings函数读取工程的配置。
    # get_project_settings会首先判断是否设置了SCRAPY_SETTINGS_MODULE环境变量，这个环境变量用来指定工程的配置
    # 模块。稍后会用这个环境变量加载工程的配置。
    # 如果没有这个环境变量，则会调用init_env来初始化环境变量
    process = CrawlerProcess(get_project_settings())
    process.crawl('233_networkSchool')
    # 有多个爬虫的话,依次往下写就可以,只需要更改爬虫名称即可
    # process.crawl('B_spider')
    # process.crawl('C_spider')
    process.start()
