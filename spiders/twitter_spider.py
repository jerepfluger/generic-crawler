from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from spiders.spider import Spider


class TwitterSpider(Spider):
    def __init__(self, spider_name):
        super(TwitterSpider, self).__init__(spider_name)

    def process_task(self, crawling, web_driver_pool):
        # proxy = self.get_proxy(crawling)

        driver = web_driver_pool.acquire(None, self._config.get('webdriver'))
        driver.get("http://www.twitter.com")
        login_button = driver.find_element_by_xpath('//a[@data-testid="loginButton"]')
        login_button.click()
        username_input = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
        username_input.send_keys(crawling['data']['username'])
        password_input = driver.find_element_by_xpath('//input[@name="session[password]"]')
        password_input.send_keys(crawling['data']['password'])
        password_input.submit()

        tweet_text = driver.find_element_by_xpath('//br[@data-text="true"]')
        tweet_text.send_keys(crawling['data']['tweet'])
        tweet_button = driver.find_element_by_xpath('//div[@data-testid="tweetButtonInline"]/div/span/span')
        tweet_button.click()

        return
        # with open("testing.txt", 'w+') as file:
        #     file.write(data)
