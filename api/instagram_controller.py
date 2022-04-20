import json

from flask import Response as FlaskResponse
from flask import request

from helpers.logger import refresh_uow, logger
from request.response import Response as EntityResponse
from spiders.instagram_spider import InstagramSpider
from webdrivers.webdriver import WebDriver
from . import routes


@routes.route("/generic-crawler/crawl/instagram", methods=["POST"])
def basic_instagram_crawler():
    crawling_data = json.loads(request.data)
    instagram_webdriver = WebDriver()
    refresh_uow()

    spider = InstagramSpider('instagram')

    logger.info('Start Crawling stage...')
    result = None
    try:
        result = spider.start(crawling_data, instagram_webdriver)
    except Exception as ex:
        result = EntityResponse(ex.message if hasattr(ex, 'message') else ex, 500)
    finally:
        spider.stop()
        return FlaskResponse(json.dumps(result, default=lambda o: o.__dict__), status=result.status,
                             mimetype='application/json')
