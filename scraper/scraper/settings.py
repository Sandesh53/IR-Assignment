BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    'scraper.middlewares.SeleniumMiddleware': 543,
}

AUTOTHROTTLE_ENABLED = True

ITEM_PIPELINES = {
    'scraper.pipelines.ElasticCleanPipeline': 300,
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 32
CONCURRENT_REQUESTS_PER_IP = 32
DOWNLOAD_DELAY = 0.5  # Reduce delay
AUTOTHROTTLE_ENABLED = True
