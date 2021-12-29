from datetime import datetime

import psutil
from pylru import lrucache
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions

from helpers import config as config_global
from helpers.logger import logger


class ChromeWebdriver:
    @staticmethod
    def create(config, proxy=None):
        logger.info("Creating Chromium Web Driver")
        options = ChromeOptions()
        options.binary_location = config.get_string('chrome-binary')
        options.add_argument('headless')
        options.add_argument('hide-scrollbars')
        options.add_argument('disable-gpu')
        options.add_argument('no-sandbox')
        options.add_argument('data-path={}'.format(config.get_string('chromium.data-path')))
        options.add_argument('disk-cache-dir={}'.format(config.get_string('chromium.cache-dir')))
        options.add_argument('disable-infobars')
        # Disable web security for get ember components via execute-scripts
        options.add_argument('disable-web-security')
        if proxy:
            options.add_argument('proxy-server={}:{}'.format(proxy.host, proxy.port))

        return webdriver.Chrome(chrome_options=options)


class FirefoxWebdriver:
    @staticmethod
    def create(config, proxy=None):
        proxy = proxy
        logger.info("Creating Firefox Web Driver")

        options = FirefoxOptions()
        options.binary_location = config.get_string('firefox-binary')
        # options.add_argument('--headless')
        options.add_argument('--new_instance')

        firefox_profile = webdriver.FirefoxProfile()
        #  https://developer.mozilla.org/en-US/docs/Mozilla/Preferences/Mozilla_networking_preferences
        firefox_profile.set_preference('browser.cache.disk.enable', 'true')
        firefox_profile.set_preference('browser.cache.memory.enable', 'true')
        firefox_profile.set_preference('browser.cache.disk.parent_directory', config.get_string('firefox.cache-dir'))
        # https://github.com/mozilla/geckodriver/issues/517#issuecomment-286701282
        firefox_profile.set_preference("browser.tabs.remote.autostart", "false")
        firefox_profile.set_preference("browser.tabs.remote.autostart.1", "false")
        firefox_profile.set_preference("browser.tabs.remote.autostart.2", "false")
        firefox_profile.set_preference("browser.tabs.remote.force-enable", "false")
        # more settings
        firefox_profile.set_preference("dom.ipc.processCount", "1")
        firefox_profile.set_preference("browser.sessionstore.interval", "50000000")
        firefox_profile.set_preference("browser.sessionstore.max_resumed_crashes", "0")
        firefox_profile.set_preference("browser.sessionstore.max_tabs_undo", "0")
        firefox_profile.set_preference("browser.sessionstore.max_windows_undo", "0")
        firefox_profile.set_preference("dom.popup_maximum", 0)
        firefox_profile.set_preference("privacy.popups.showBrowserMessage", False)
        firefox_profile.set_preference("privacy.popups.disable_from_plugins", 3)
        # Proxy
        if proxy:
            logger.info("Setting proxy values to http {} and port {}".format(proxy.host, proxy.port))
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_proxy = "{}:{}".format(proxy.host, proxy.port)
            firefox_capabilities['proxy'] = {
                "proxyType": "MANUAL",
                "httpProxy": firefox_proxy,
                "ftpProxy": firefox_proxy,
                "sslProxy": firefox_proxy
            }

            return webdriver.Firefox(firefox_profile=firefox_profile, firefox_options=options, log_path="/dev/null",
                                     capabilities=firefox_capabilities)

        return webdriver.Firefox(firefox_profile=firefox_profile, firefox_options=options, log_path="/dev/null")


class WebDriver:
    FIREFOX = 'firefox'
    CHROMIUM = 'chromium'

    web_driver_creators = {
        FIREFOX: FirefoxWebdriver.create,
        CHROMIUM: ChromeWebdriver.create
    }

    def __init__(self, config=config_global.conf.get_config('web-driver')):
        self.config = config
        self.drivers = lrucache(self.config.get_int('cache.max-entries'), callback=self.on_eviction)
        self.stopped = False
        self.last_time_used = datetime.now()

    def acquire(self, proxy, type):
        if not self.stopped and type in self.web_driver_creators:
            key = WebDriver.key_from(proxy, type)
            driver = self.drivers.get(key, self.web_driver_creators.get(type)(self.config, proxy))
            self.drivers[key] = driver
            self.last_time_used = datetime.now()
            return driver
        else:
            return None

    def release(self, driver):
        pass

    @staticmethod
    def force_quit(driver):

        try:
            driver.quit()
        except Exception as e:
            logger.error('Failed trying to quit a Web Driver process.. killing the driver..', e)
            d = psutil.Process(driver.service.process.pid)
            [browser.kill() for browser in d.children()]
            d.kill()

    def clear_if_not_used(self):
        delta = datetime.now() - self.last_time_used
        if delta.total_seconds() > self.config.get_int('cache.max-age.seconds') and len(self.drivers) > 0:
            [WebDriver.force_quit(driver) for k, driver in self.drivers.items()]
            self.drivers.clear()

    def stop(self):
        """Stops the webdriver pool, quits all started processes and prevent
        creation of further processes."""
        self.stopped = True
        try:
            for proxy, driver in self.drivers.items():
                logger.info('Trying to quit driver for proxy: {}'.format(proxy))
                WebDriver.force_quit(driver)
        except:
            logger.exception('Failed trying to kill a Web Driver process')

    @staticmethod
    def on_eviction(key, driver):
        logger.info("removing previous driver: {}, {}".format(key, driver))
        WebDriver.force_quit(driver)

    @staticmethod
    def key_from(proxy, type):
        proxy_key = "%s-%s-%s" % (proxy.host, proxy.port, proxy.supplier) if proxy is not None else "none-proxy"
        return "%s-%s" % (type, proxy_key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
