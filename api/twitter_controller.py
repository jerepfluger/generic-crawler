import json

from flask import request

from helpers.logger import refresh_uow, logger
from spiders.spider_factory import SpiderFactory
from webdrivers.webdriver import WebDriver
from . import routes


@routes.route("/generic-crawler/crawl/twitter", methods=["POST"])
def basic_twitter_crawler():
    crawling_data = json.loads(request.data)
    twitter_webdriver = WebDriver()
    refresh_uow()
    spider = SpiderFactory.choose('twitter')

    logger.info('Processing search')  # TODO: Here I could set more particular info
    logger.info('Start Crawling stage...')
    try:
        spider.start(crawling_data, twitter_webdriver)
    finally:
        spider.stop()
