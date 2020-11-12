from spiders.spider import Spider


class TwitterSpider(Spider):
    def __init__(self, spider_name):
        super(TwitterSpider, self).__init__(spider_name)

    def process_task(self, crawling, web_driver_pool):
        driver = None

        # proxy = {'proxy': 'no-proxy'}
        # proxy = self.get_proxy(crawling)

        driver = web_driver_pool.acquire(None, self._config.get('webdriver'))
        return driver.get("http://www.google.com")
        # with open("testing.txt", 'w+') as file:
        #     file.write(data)
