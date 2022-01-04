import os
import random
import time
from datetime import datetime
from pathlib import Path

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import By
from selenium.webdriver.support.wait import WebDriverWait

from exceptions.exceptions import NonExistentCombinationsException
from helpers.logger import logger
from repositories.instagram_crawling_repository import InstagramCrawlingRepository
from request.response import Response, InstagramDetailedResponse
from spiders.spider import Spider

emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '🥲', '☺️', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰',
          '😘', '😗', '😙', '😚', '😋', '😛']


def _two_tags_combination(tags):
    result = []
    for i in range(len(tags) - 1):
        result.append([tags[i], tags[i + 1]])
        if i + 2 < len(tags):
            result.append([tags[i], tags[i + 2]])
    result.append([tags[0], tags[-1]])

    return result


def _three_tags_combination(tags):
    result = []
    for i in range(len(tags) - 2):
        result.append([tags[i], tags[i + 1], tags[i + 2]])
        if i + 3 < len(tags) - 1:
            result.append([tags[i], tags[i + 2], tags[i + 3]])
        result.append([tags[0], tags[-1], tags[-2]])

    return result


def _five_tags_combination(tags):
    result = []
    for i in range(len(tags) - 4):
        result.append([tags[i], tags[i + 1], tags[i + 2], tags[i + 3], tags[i + 4]])
        if i + 5 < len(tags) - 3:
            result.append([tags[i], tags[i + 2], tags[i + 3], tags[i + 4], tags[i + 5]])
        result.append([tags[0], tags[-1], tags[-2]])

    return result


def _create_combinations(tags, tags_amount):
    if tags_amount == 1:
        return tags
    if tags_amount == 2:
        return _two_tags_combination(tags)
    if tags_amount == 3:
        return _three_tags_combination(tags)
    if tags_amount == 5:
        return _five_tags_combination(tags)

    raise NonExistentCombinationsException('There\'s no algorithm created for {} tags combinatory'.format(tags_amount))


def _takescreenshot(driver):
    route_to_folder = '{}/{}'.format(Path.home(), 'Repos/python/generic-crawler/screenshots/')
    screenshot_time = datetime.now().strftime("%Y:%m:%d %H:%m:%S")
    if not os.path.exists(route_to_folder):
        os.mkdir(route_to_folder)
    driver.save_screenshot('{}/screenshot-{}.png'.format(route_to_folder, screenshot_time))
    logger.info('Screenshot saved in %s/%s', route_to_folder, screenshot_time)


def _save_instagram_record(crawling, tagging_count, percentage):
    data = crawling['data']
    InstagramCrawlingRepository().add_record(data['draw'], data['account_draw'], tagging_count, percentage,
                                             data['tags_needed'], False, False)


class InstagramSpider(Spider):
    def __init__(self, spider_name):
        super(InstagramSpider, self).__init__(spider_name)

    def process_task(self, crawling, web_driver_pool):
        driver = web_driver_pool.acquire(None, self._config.get('webdriver'))
        # Go to instagram website
        driver.get(self._config.get('base_url'))

        # Waiting for login page to be fully loaded
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, self._config.get('html_location.username_input'))))
        self._login(driver, crawling)

        # Waiting for user to be fully logged in and redirecting to
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, self._config.get('html_location.user_avatar'))))
        driver.get("{}{}".format(self._config.get('base_url'), crawling['data']['draw']))

        tagging_response = None
        if crawling['data']['needs_tagging']:
            try:
                tagging_response = self._tag_friends(driver, crawling)
            except Exception as ex:
                _takescreenshot(driver)
                tagging_response = Response(str(ex), 500)

        follow_response = None
        if crawling['data']['needs_follow']:
            try:
                follow_response = self._follow_account(driver)
            except Exception as ex:
                follow_response = Response(str(ex), 500)

        like_response = None
        if crawling['data']['needs_like']:
            try:
                like_response = self._like_post(driver)
            except Exception as ex:
                like_response = Response(str(ex), 500)

        if crawling['data']['needs_post_story']:
            self._post_to_story(driver)

        return InstagramDetailedResponse(tagging_response, follow_response, like_response, 200)

    def _login(self, driver, crawling):
        control = self.complete_login_data(crawling, driver)
        control.submit()
        try:
            driver.find_element_by_id("slfErrorAlert")
            logger.error("Will take a nap for 30 sec and try again. Hope it works")
            time.sleep(30)
            control = self.complete_login_data(crawling, driver)
            control.submit()
        except NoSuchElementException:
            pass

    def complete_login_data(self, crawling, driver):
        username_input = driver.find_element_by_xpath(self._config.get('html_location.username_input'))
        username_input.send_keys(crawling['data']['username'])
        password_input = driver.find_element_by_xpath(self._config.get('html_location.password_input'))
        password_input.send_keys(crawling['data']['password'])
        return password_input

    def _tag_friends(self, driver, crawling):
        subset_count = 0
        combinations_array = _create_combinations(crawling['data']['friends'], crawling['data']['tags_needed'])

        for subset in combinations_array:
            comment_button = driver.find_element_by_xpath(self._config.get('html_location.comment_button'))
            comment_button.click()
            # driver.find_element_by_xpath(self._config.get('html_location.text_area')).click()
            comment_area = driver.switch_to.active_element
            comment_area.send_keys(' '.join(subset))
            time.sleep(3)
            comment_area.send_keys(" ")

            if crawling['data']['needs_message']:
                comment_area.send_keys(crawling['data']['message'])
            elif self._config.get('webdriver') != 'chromium':
                comment_area.send_keys(random.choice(emojis))

            post_button = driver.find_element_by_xpath(self._config.get('html_location.submit_button'))
            post_button.click()
            time.sleep(1.5)

            try:
                driver.find_element_by_xpath(self._config.get('html_location.blocked_banner'))
                _takescreenshot(driver)
                tagging_count = '{}/{}'.format(subset_count, len(combinations_array))
                percentage = subset_count * 100 / len(combinations_array)
                logger.error('Last element unable to be posted was -> %s', subset)
                logger.error('From a total of %s and this represent the %s percentage', tagging_count, percentage)

                _save_instagram_record(crawling, tagging_count, percentage)

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
        try:
            follow_button = driver.find_element_by_xpath(self._config.get('html_location.follow_button'))
            follow_button.click()
            logger.info('Successfully Following the account')
        except NoSuchElementException:
            logger.info('Unable to locate Follow button. Searching if already following account')
            try:
                driver.find_element_by_xpath(self._config.get('html_location.unfollow_button'))
                logger.info('Already following account')
            except NoSuchElementException:
                logger.error('Unable to locate Follow/Unfollow button. xpath seems to be corrupted')

        return Response('Successfully Following the account', 200)

    def _like_post(self, driver):
        try:
            like_state = driver.find_element_by_xpath(self._config.get('html_location.like_state')).get_attribute(
                'aria-label')
            if like_state == 'Like' or like_state == 'Me gusta':
                like_button = driver.find_element_by_xpath(self._config.get('html_location.like_button'))  # Like button
                like_button.click()
                logger.info('Successfully liked the post')
            elif like_state == 'Unlike' or like_state == 'Ya no me gusta':
                logger.info('Already liked post')
            else:
                logger.error("No idea what could be going on in here")
                return Response('Unable to like post', 404)
        except NoSuchElementException:
            logger.error('Unable to locate Like button')
            return Response('Unable to like post', 404)

        return Response('Successfully liked post', 200)

    def _post_to_story(self, driver):
        # share_button = driver.find_element_by_xpath('//button[@class="wpO6b  "]')
        # share_button.click()
        # WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, './/div[@aria-label="Compartir"]')))
        # TODO: Here we should click the option that publishes this to our own story. After doing that, we should tag the account

        pass  # THIS OPTION IS NOT YET AVAILABLE!
