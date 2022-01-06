# coding=utf-8
import datetime
import gzip
import os
import sys
from abc import ABCMeta, abstractmethod

from pyhocon import ConfigFactory
from selenium.webdriver.remote.remote_connection import LOGGER

import helpers.config as config_provider
from helpers.file_helper import create_dir_if_not_exists
from helpers.logger import logger
from helpers.measure_time import measure_time

LOGGER.setLevel(30)

ENDIANNESS = sys.byteorder  # this should be a global or class variable to avoid a syscall for every random


class Spider(metaclass=ABCMeta):

    @staticmethod
    def stop():
        Spider.__stopped = True

    def __init__(self, spider_name):
        self.__config = Spider._load_config(spider_name)
        self.__data_base_path = self.__config.get_string('data-base-path')
        self._max_retry_task = self.__config.get_int('max-retry-task', 1)
        self._proxy_list = []
        self.stopped = False
        self.url_base = None
        create_dir_if_not_exists(self.__data_base_path)

    @property
    def proxy_list(self):
        return self._proxy_list

    @measure_time
    def start(self, crawling, driver_pool):
        Spider.__stopped = False
        self.init_proxy_list(crawling)

        name = 'report id {} and schedule id {} and task id {}'.format(crawling['report_id'],
                                                                       crawling['search']['schedule_id'],
                                                                       crawling['search']['task_id'])
        logger.info('Starting crawling for {}'.format(name))

        self.prepare_spider(crawling)

        spider_result = self.process_task(crawling, driver_pool)

        logger.info('Spider finish. {}'.format(spider_result))
        return spider_result

    # @measure_time
    # @retry(lambda x: x is not None, 3)
    @abstractmethod
    def process_task(self, crawling, driver_pool):
        pass

    @property
    def _config(self):
        return self.__config

    def _data_base_path(self, schedule_id, task_id):
        today = datetime.datetime.utcnow().date().strftime("%Y-%m-%d")
        return os.path.join(self.__data_base_path, today, str(schedule_id), str(task_id))

    @staticmethod
    def _load_config(spider_name):
        # The config must be loaded again with `config_provider.load_config()` since the method `get_config`
        # and `fallback` override `config_provider.conf` object
        crawling_conf = config_provider.load_config()['crawling']
        return crawling_conf.get_config(spider_name,
                                        ConfigFactory.from_dict({})) \
            .with_fallback(crawling_conf)

    def check_and_create_dir(self, base_path):
        try:
            os.makedirs(base_path)
        except OSError:
            if not os.path.isdir(base_path):
                raise

    def save_html(self, dest_id, schedule_id, task_id, content, extension="html", page_number=0):
        base_path = self._data_base_path(schedule_id, task_id)
        self.check_and_create_dir(base_path)

        filename = '{}_page_{}.{}.gz'.format(str(dest_id), str(page_number), extension)
        file_path = os.path.join(base_path, filename)
        with gzip.open(file_path, 'wb') as f:
            f.write(content)

        return file_path

    def select_driver(self, crawling, web_driver_pool):
        rnd_proxy = Spider._get_random_proxy(crawling)
        return rnd_proxy, web_driver_pool.acquire(rnd_proxy, self._config.get('webdriver'))

    def init_proxy_list(self, crawling):
        if crawling['proxy']['enabled']:
            self._proxy_list = crawling.proxy.addresses

    def remove_proxy(self, proxy):
        if self._proxy_list:
            self._proxy_list.remove(proxy)

    def _get_random_proxy(self):
        if self.proxy_list:
            size = len(self.proxy_list)
            rnd = int.from_bytes(os.urandom(2), ENDIANNESS) % size
            rnd_proxy = self.proxy_list[rnd]
            logger.info('Using Proxy - host: {} port: {}'.format(rnd_proxy.host, rnd_proxy.port))
        else:
            rnd_proxy = None

        return rnd_proxy

    @abstractmethod
    def prepare_spider(self, crawling):
        pass
