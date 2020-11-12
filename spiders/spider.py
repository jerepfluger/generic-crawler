# coding=utf-8
import datetime
import gzip
import os
import sys
from abc import ABCMeta, abstractmethod

import requests
from pyhocon import ConfigFactory
from requests.exceptions import ProxyError, ConnectTimeout
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.remote_connection import LOGGER

import helpers.config as config_provider
from exceptions.exceptions import MalformedHtmlException, ProxyException, BannedProxyException, TimeoutProxyException, \
    ConnectionRefusedException
from helpers.file_helper import create_dir_if_not_exists
from helpers.logger import logger
from helpers.measure_time import measure_time
from helpers.retry_function import retry

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

    @staticmethod
    def success_result(result):
        return result.successful

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

    @staticmethod
    def fail_on_malformed_html(driver, id_selector):
        try:
            driver.find_element_by_id(id_selector)
        except NoSuchElementException:
            raise MalformedHtmlException

    def select_driver(self, crawling, web_driver_pool):
        rnd_proxy = Spider._get_random_proxy(crawling)
        return rnd_proxy, web_driver_pool.acquire(rnd_proxy, self._config.get('webdriver'))

    def init_proxy_list(self, crawling):
        if crawling['proxy']['enabled']:
            self._proxy_list = crawling.proxy.addresses

    def remove_proxy(self, proxy):
        if self._proxy_list:
            self._proxy_list.remove(proxy)

    @retry(max_attempts=6, exception_on_error=ProxyException)
    def get_proxy(self, crawling):
        if crawling['proxy']['enabled']:
            rnd_proxy = self._get_random_proxy()
            if not self.check_proxy_health(rnd_proxy):
                return rnd_proxy
        else:
            return None

    def _get_random_proxy(self):
        if self.proxy_list:
            size = len(self.proxy_list)
            rnd = int.from_bytes(os.urandom(2), ENDIANNESS) % size
            rnd_proxy = self.proxy_list[rnd]
            logger.info('Using Proxy - host: {} port: {}'.format(rnd_proxy.host, rnd_proxy.port))
        else:
            rnd_proxy = None

        return rnd_proxy

    @measure_time
    def check_proxy_health(self, proxy):
        try:
            proxies = {
                'http': 'http://{}:{}'.format(proxy.host, proxy.port),
                'https': 'http://{}:{}'.format(proxy.host, proxy.port),
            }

            logger.debug("Checking proxy health -> {}:{}".format(proxy.host, proxy.port))
            r = requests.get(self.url_base, proxies=proxies, timeout=30)
            if r.status_code == 403:
                logger.warning('The IP proxy {}:{} is banned'.format(proxy.host, proxy.port))
                self.remove_proxy(proxy)
                raise BannedProxyException(proxy.host)
            logger.debug("Proxy health is OK ;)")
        except ConnectTimeout:
            logger.warning(
                "Proxy {}:{} seems to be slow. Will remove it from proxy list".format(proxy.host, proxy.port))
            self.remove_proxy(proxy)
            raise TimeoutProxyException(proxy.host)
        except ProxyError:
            logger.error("Connection refused for proxy: {}:{}".format(proxy.host, proxy.port))
            self.remove_proxy(proxy)
            raise ConnectionRefusedException(proxy.host)
        except Exception as ex:
            logger.error("No proxies", exc_info=ex)
            raise ex


class SpiderResult(object):

    def __init__(self, crawling, successful, crawling_pages=[], message='-'):
        self.__crawling = crawling
        self.__successful = successful
        self.__crawling_pages = crawling_pages
        self.__message = message

    @property
    def crawling(self):
        return self.__crawling

    @property
    def successful(self):
        return self.__successful

    @property
    def crawling_pages(self):
        return self.__crawling_pages

    @property
    def message(self):
        return self.__message

    def __str__(self):
        return 'SpiderResult(Crawling ID: {}, Successful: {}, Files quantity: {}, Message: {})' \
            .format(self.crawling.id, self.successful, len(self.crawling_pages), self.message)

    @staticmethod
    def one_successful(crawling, crawling_pages, message=''):
        return SpiderResult(crawling, successful=True, crawling_pages=crawling_pages, message=message)

    @staticmethod
    def one_failed(crawling, message):
        return SpiderResult(crawling, successful=False, message=message)
