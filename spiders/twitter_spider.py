from spiders.spider import Spider


class TwitterSpider(Spider):
    def __init__(self, spider_name):
        super(TwitterSpider, self).__init__(spider_name)

    def process_task(self, crawling, web_driver_pool):
        # proxy = self.get_proxy(crawling)

        driver = web_driver_pool.acquire(None, self._config.get('webdriver'))
        driver.get("http://www.twitter.com")
        return
        # with open("testing.txt", 'w+') as file:
        #     file.write(data)
