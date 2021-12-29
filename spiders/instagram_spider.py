import itertools
import random
import time

from selenium.common.exceptions import NoSuchElementException

from entities.response import Response
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
        driver.get(INSTAGRAM_URL)

        # Waiting for login page to be fully loaded
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//input[@name="username"]')))
        username_input = driver.find_element_by_xpath('//input[@name="username"]')
        username_input.send_keys(crawling['data']['username'])
        password_input = driver.find_element_by_xpath('//input[@name="password"]')
        password_input.send_keys(crawling['data']['password'])
        password_input.submit()

        # Waiting for user to be fully logged in
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, './/img[@data-testid="user-avatar"]')))
        driver.get("{}{}".format(INSTAGRAM_URL, crawling['data']['desired_post']))

        if crawling['data']['needs_tagging']:
            subset_count = 0
            for subset in itertools.combinations(crawling['data']['friends'], crawling['data']['tags_needed']):
                comment_button = driver.find_element_by_xpath('//span[@class="_15y0l"]/button')  # Comment button
                comment_button.click()

                comment_area = driver.switch_to.active_element
                comment_area.send_keys(' '.join(subset))
                time.sleep(3)
                comment_area.send_keys(" ")
                comment_area.send_keys(random.choice(emojis))
                if crawling['data']['needs_message']:
                    comment_area.send_keys(crawling['data']['message'])

                post_button = driver.find_element_by_xpath('//button[@type="submit"]')
                post_button.click()
                time.sleep(1)

                try:
                    driver.find_element_by_xpath('//div[@class="JBIyP"]')
                    logger.error('Last element able to be posted was -> {}'.format(subset))
                    logger.error('From a total of {}/{} and this represent the {} percentage'.format(subset_count, len(crawling['data']['friends']), subset_count * 100 / len(crawling['data']['friends'])))
                    # TODO: Aca posiblemente podes hacer un sleep mas largo en caso de fallo y poner un timeout a los X reintentos
                    # TODO: Otra opcion sería hacer un skip de la cuenta que estamos por taggear, pero esa logica seria un poco mas rebuscada
                    return Response('EL PROCEDIMIENTO TERMINO DEFECTUOSAMENTE!', 429)
                except NoSuchElementException:
                    subset_count += 1
                    logger.info('Successfully commented %s/%s with tags %s and message %s', subset_count, len(crawling['data']['friends']), subset, crawling['data']['message'])
                    pass

                # Waiting for comment to be published
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//textarea[@data-testid="post-comment-text-area"]')))

                time.sleep(40)

        # if crawling['data']['needs_post_story']:
        #     share_button = driver.find_element_by_xpath('//button[@class="wpO6b  "]')
        #     share_button.click()
        #     WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, './/div[@aria-label="Compartir"]')))
        #     TODO: Here we should click the option that publishes this to our own story
        #     TODO: After doing that, we should tag the account
        #     TODO: THIS OPTION IS NOT YET AVAILABLE!

        if crawling['data']['needs_follow']:
            follow_button = driver.find_element_by_xpath('//button[text()="Follow"]')
            follow_button.click()
            logger.info('Successfully Following the account')

        if crawling['data']['needs_like']:
            like_button = driver.find_element_by_xpath('//span[@class="fr66n"]//*[name()="svg"]')  # Like button
            like_state = like_button.get_attribute('aria-label')
            if like_state == 'Like':
                like_button.click()
                logger.info('Successfully liked the post')

        return Response('EL PROCEDIMIENTO TERMINO EXITOSAMENTE!', 200)
