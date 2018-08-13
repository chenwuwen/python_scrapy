# -*- coding: utf-8 -*-

# Scrapy settings for python_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'python_scrapy'

SPIDER_MODULES = ['python_scrapy.spiders']
NEWSPIDER_MODULE = 'python_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'python_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
# 不访问网站ROBOTS.txt文件,以解决网站反爬虫限制,是否遵守robots协议，默认为Ture
ROBOTSTXT_OBEY = False

# 修改默认的输出编码方式(不设置的话,返回json中文乱码[xe4\xbd\x9c\xe6\x88])
FEED_EXPORT_ENCODING = 'utf-8'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 控制并发数,默认是16，并发是指同时处理的request的数量
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 延迟设置，防止速度过快被服务器检测到,设置延迟下载可以避免被发现
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16
# Scrapy框架参数项目参数设置
# Disable cookies (enabled by default)
# 禁用cookie追踪降低被发现几率
# 除非您 真的 需要，否则请禁止cookies。在进行通用爬取时cookies并不需要， (搜索引擎则忽略cookies)。禁止cookies能减少CPU使用率及Scrapy爬虫在内存中记录的踪迹，提高性能。
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'python_scrapy.middlewares.PythonScrapySpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# 启用middlewares
DOWNLOADER_MIDDLEWARES = {
    'python_scrapy.middlewares.PythonScrapyDownloaderMiddleware': 543,
    # 禁用系统useragent，None表示禁用，数字越小优先级越高
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 开启pipeline
ITEM_PIPELINES = {
    'python_scrapy.pipelines.PythonScrapyPipeline': 300,
    'python_scrapy.pipelines.NetWorkSchoolPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# 爬取深度,默认直接爬取完
DEPTH_LIMIT = 100
