import json
import time
from threading import Thread
from time import sleep

import helpers.config as config_global
from helpers.logger import logger, refresh_uow
from spiders.spider import Spider
from webdrivers.webdriver import WebDriver


class Worker(Thread):

    def __init__(self, crawling_data, spider_name, config=config_global.conf):
        super(Worker, self).__init__()
        self._config = config
        self._stopped = False
        self.__poll_interval = self._config.get_int('worker.poll_interval')
        self.__active_bots = [spider_key for spider_key in
                              self._config.get_list('active-spiders')]
        self._crawling_data = crawling_data
        self._spider_name = spider_name

    def stop(self):
        logger.info("Stopping worker...")
        self._stopped = True
        Spider.stop()

    def run(self):
        with WebDriver as driver_pool:
            while not self._stopped:
                try:
                    driver_pool.clear_if_not_used()
                    refresh_uow()
                    self.process(self._crawling_data, driver_pool)
                except Exception as e:
                    logger.error('Unexpected Error. Good bye!!', e)
                    break
        logger.info("Shutdown!")

    def process(self, crawling, driver_pool):
        try:
            Spider(self._spider_name).start(crawling, driver_pool)
        except Exception as e:
            logger.error('Failed trying to process crawling {}'.format(crawling.id), e)

    # def notify_success(self, crawling, crawler_result):
    #     try:
    #         body = {
    #             "crawling_id": crawling.id,
    #             "schedule_id": crawling.search.schedule_id,
    #             "task_id": crawling.search.task_id,
    #             "ota": BotResolver.get_key_config_by_id(crawling.bot.id)['ota'],
    #             "status": crawler_result.status,
    #             "user_id": crawling.search.user.id if crawling.search.user is not None else None,
    #             "message": crawler_result.message,
    #             "failed_files": crawler_result.parser_result.failed_files,
    #             "results": crawler_result.parser_result.bulks
    #         }
    #
    #         logger.info('Hotels to be saved into Capitan {}'.format(
    #             json.dumps(list(map(lambda result: result.hotel_id, body['results'])))))
    #
    #         # response = self._captain_global_client.send_result(body, silent_error=True)
    #         logger.info('Summary of the execution: Crawling ID: {}, Schedule ID: {}, Task ID: {}, OTA: {}, '
    #                     'Status: {}, Message: {}, Results: {}, Failed files: {}'
    #                     .format(crawling.id, crawling.search.schedule_id, crawling.search.task_id, body['ota'],
    #                             crawler_result.status, crawler_result.message,
    #                             len(crawler_result.parser_result.bulks),
    #                             len(crawler_result.parser_result.failed_files)))
    #
    #         # if response is not None:
    #         #     logger.info(
    #         #         'Captain Global response - code: {} - body:{}'.format(response.status_code, response.text))
    #     except Exception as e:
    #         logger.error('Failed trying to process crawling {}'.format(crawling.id), e)
