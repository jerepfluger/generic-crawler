import itertools
import random
import time

from selenium.common.exceptions import NoSuchElementException

from request.response import Response
from helpers.logger import logger

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import By

from spiders.spider import Spider


INSTAGRAM_URL = "https://www.instagram.com/"

emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '🥲', '☺️', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰',
          '😘', '😗', '😙', '😚', '😋', '😛']


class InstagramSpider(Spider):
    def __init__(self, spider_name):
        super(InstagramSpider, self).__init__(spider_name)

    def process_task(self, crawling, web_driver_pool):
        driver = web_driver_pool.acquire(None, self._config.get('webdriver'))
        # Go to instagram website
        driver.get(INSTAGRAM_URL)

        # Waiting for login page to be fully loaded
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, self._config.get('html_location.username_input'))))
        self._login(driver, crawling)

        # Waiting for user to be fully logged in and redirecting to
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, self._config.get('html_location.user_avatar'))))
        driver.get("{}{}".format(INSTAGRAM_URL, crawling['data']['desired_post']))

        if crawling['data']['needs_tagging']:
            self._tag_friends(driver, crawling)

        if crawling['data']['needs_follow']:
            self._follow_account(driver)

        if crawling['data']['needs_like']:
            self._like_post(driver)

        if crawling['data']['needs_post_story']:
            self._post_to_story(driver)

        return Response('Procedure ended up successfully!', 200)

    def _login(self, driver, crawling):
        username_input = driver.find_element_by_xpath(self._config.get('html_location.username_input'))
        username_input.send_keys(crawling['data']['username'])

        password_input = driver.find_element_by_xpath(self._config.get('html_location.password_input'))
        password_input.send_keys(crawling['data']['password'])

        password_input.submit()

    def _tag_friends(self, driver, crawling):
        subset_count = 0
        combinations_array = list(itertools.combinations(crawling['data']['friends'], crawling['data']['tags_needed']))

        for subset in combinations_array:
            comment_button = driver.find_element_by_xpath(".//span[@class='_15y0l']/button")
            # comment_button = driver.find_element_by_xpath(self._config.get('html_location.comment_button'))
            comment_button.click()

            comment_area = driver.switch_to.active_element
            comment_area.send_keys(' '.join(subset))
            time.sleep(3)
            comment_area.send_keys(" ")
            comment_area.send_keys(random.choice(emojis))
            if crawling['data']['needs_message']:
                comment_area.send_keys(crawling['data']['message'])

            post_button = driver.find_element_by_xpath(self._config.get('html_location.submit_button'))
            post_button.click()
            time.sleep(1)

            try:
                driver.find_element_by_xpath(self._config.get('html_location.blocked_banner'))
                logger.error('Last element able to be posted was -> {}'.format(subset))
                logger.error('From a total of {}/{} and this represent the {} percentage'.format(subset_count,
                                                                                                 len(combinations_array),
                                                                                                 subset_count * 100 / len(combinations_array)))
                # Aca posiblemente podes hacer un sleep mas largo en caso de fallo y poner un timeout a los X reintentos
                # Otra opcion sería hacer un skip de la cuenta que estamos por taggear, pero esa logica seria un poco mas rebuscada
                return Response('Procedure ended up with ERRORS!', 429)
            except NoSuchElementException:
                subset_count += 1
                logger.info('Successfully commented %s/%s with tags %s and message %s', subset_count,
                            len(combinations_array), subset, crawling['data']['message'])
                pass

            # Waiting for comment to be published
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, self._config.get('html_location.text_area'))))

            if subset_count < 419:
                time.sleep(40)
            else:
                logger.info('Already running for 5 hours. Seems comments enough by this time')

    def _follow_account(self, driver):
        if not self._already_following(driver):
            try:
                follow_button = driver.find_element_by_xpath(self._config.get('html_location.follow_button'))
                follow_button.click()
                logger.info('Successfully Following the account')
            except NoSuchElementException:
                logger.error('Unable to locate Follow button')

    def _already_following(self, driver):
        try:
            driver.find_element_by_xpath(self._config.get('html_location.unfollow_button'))
        except NoSuchElementException:
            logger.info('Already following account')
            return True

        return False

    def _like_post(self, driver):
        try:
            like_button = driver.find_element_by_xpath(self._config.get('html_location.like_button'))  # Like button
            like_state = like_button.get_attribute('aria-label')
            if like_state == 'Like' or like_state == 'Me gusta':
                like_button.click()
                logger.info('Successfully liked the post')
            elif like_state == 'Unlike' or like_state == 'Ya no me gusta':
                logger.info('Still OK. Already liked post')
        except NoSuchElementException:
            logger.error('Unable to locate Like button')
            pass

    def _post_to_story(self, driver):
        # share_button = driver.find_element_by_xpath('//button[@class="wpO6b  "]')
        # share_button.click()
        # WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, './/div[@aria-label="Compartir"]')))
        # TODO: Here we should click the option that publishes this to our own story. After doing that, we should tag the account

        pass  # THIS OPTION IS NOT YET AVAILABLE!
