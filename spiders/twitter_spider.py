from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import By
from selenium.webdriver.support.wait import WebDriverWait

from spiders.spider import Spider


class TwitterSpider(Spider):
    def __init__(self, spider_name):
        super(TwitterSpider, self).__init__(spider_name)

    def process_task(self, crawling, web_driver_pool):
        # proxy = self.get_proxy(crawling)

        driver = web_driver_pool.acquire(None, self._config.get('webdriver'))
        driver.get("http://www.twitter.com")

        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//a[@data-testid="loginButton"]')))
        login_button = driver.find_element_by_xpath('//a[@data-testid="loginButton"]')
        login_button.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//input[@autocomplete="username"]')))
        username_input = driver.find_element_by_xpath('//input[@autocomplete="username"]')
        username_input.send_keys(crawling['data']['username'])
        username_input.submit()

        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//input[@autocomplete="current-password"]')))
        password_input = driver.find_element_by_xpath('//input[@autocomplete="current-password"]')
        password_input.send_keys(crawling['data']['password'])
        password_input.submit()

        tweet_text = driver.find_element_by_xpath('//br[@data-text="true"]')
        tweet_text.send_keys(crawling['data']['tweet'])
        tweet_text.submit()

        return
        # with open("testing.txt", 'w+') as file:
        #     file.write(data)
