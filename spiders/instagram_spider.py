from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from spiders.spider import Spider


class InstagramSpider(Spider):
    def __init__(self, spider_name):
        super(InstagramSpider, self).__init__(spider_name)

    def process_task(self, crawling, web_driver_pool):
        # proxy = self.get_proxy(crawling)

        driver = web_driver_pool.acquire(None, self._config.get('webdriver'))
        driver.get("https://www.instagram.com/")
        # TODO: I should set a wait here to make inputs reachable
        username_input = driver.find_element_by_xpath('//input[@name="username"]')
        username_input.send_keys(crawling['data']['username'])
        password_input = driver.find_element_by_xpath('//input[@name="password"]')
        password_input.send_keys(crawling['data']['password'])
        password_input.submit()

        driver.get("https://www.instagram.com/p/CXeJGaFlc7E/")

        # # TODO: Before posting any comment there're two clicks
        # finder = driver.find_element_by_xpath('//input[@placeholder="Buscar"]')
        # finder.send_keys(crawling['data']['searched_account'])
        #
        # searched_account = driver.find_element_by_xpath('//a[@href="/{}/"]'.format(crawling['data']['searched_account']))
        # searched_account.click()
        #
        # # TODO: Need to set a wait time here also
        # desired_post = driver.find_element_by_xpath('//a[@href="/{}/"]'.format(crawling['data']['desired_post']))
        # desired_post.click()
        text_area = driver.find_element_by_xpath('//span[@class="_15y0l"]')
        text_area.click()

        comment_area = driver.switch_to.active_element
        if crawling['data']['tag']:
            comment_area.send_keys('@')
            comment_area.send_keys(crawling['data']['friend_tag'])
            comment_area.send_keys(Keys.ARROW_DOWN)
            comment_area.send_keys(Keys.ENTER)
        comment_area.send_keys(crawling['data']['message'])
        comment_area.submit()

        return
        # with open("testing.txt", 'w+') as file:
        #     file.write(data)
