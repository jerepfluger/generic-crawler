import json

from flask import request

from helpers.logger import refresh_uow, logger
from spiders.twitter_spider import TwitterSpider
from webdrivers.webdriver import WebDriver
from . import routes


@routes.route("/generic-crawler/crawl/twitter", methods=["POST"])
def basic_twitter_crawler():
    crawling_data = json.loads(request.data)
    twitter_webdriver = WebDriver()
    refresh_uow()

    spider = TwitterSpider('twitter')
    logger.info('Start Crawling stage...')
    try:
        spider.start(crawling_data, twitter_webdriver)
    finally:
        spider.stop()
