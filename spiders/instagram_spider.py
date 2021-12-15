import itertools

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import By


from spiders.spider import Spider


class InstagramSpider(Spider):
    def __init__(self, spider_name):
        super(InstagramSpider, self).__init__(spider_name)

    def process_task(self, crawling, web_driver_pool):
        driver = web_driver_pool.acquire(None, self._config.get('webdriver'))
        driver.get("https://www.instagram.com/")

        # Waiting for login page to be fully loaded
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//input[@name="username"]')))
        username_input = driver.find_element_by_xpath('//input[@name="username"]')
        username_input.send_keys(crawling['data']['username'])
        password_input = driver.find_element_by_xpath('//input[@name="password"]')
        password_input.send_keys(crawling['data']['password'])
        password_input.submit()

        # Waiting for user to be fully logged in
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, './/img[@data-testid="user-avatar"]')))
        driver.get("https://www.instagram.com/p/CXeJGaFlc7E/")

        text_area = driver.find_element_by_xpath('//span[@class="_15y0l"]')  # Comment button
        text_area.click()

        comment_area = driver.switch_to.active_element
        if crawling['data']['tag']:
            for subset in itertools.combinations(crawling['data']['friends'], crawling['data']['tags_needed']):
                comment_area.send_keys(' '.join(subset))
                comment_area.send_keys(" ")
                if crawling['data']['needs_message']:
                    comment_area.send_keys(crawling['data']['message'])
                comment_area.submit()
                # Waiting for comment to be published
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, './/button[@data-testid="post-comment-input-button"]')))

        # if crawling['data']['needs_story']:
        #     share_button = driver.find_element_by_xpath('//button[@class="wpO6b  "]')
        #     share_button.click()
        #     WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, './/div[@aria-label="Compartir"]')))
        #     TODO: Here we should click the option that publishes this to our own story
        #     TODO: After doing that, we should tag the account
