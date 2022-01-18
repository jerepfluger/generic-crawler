import random
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import By
from selenium.webdriver.support.wait import WebDriverWait

from exceptions.exceptions import BannedSpiderException, NoneActiveDrawsException
from helpers.algorithms.instagram_combinatory import create_tags_combinations
from helpers.logger import logger
from repositories.instagram_crawling_repository import InstagramCrawlingRepository
from repositories.instagram_draws_repository import InstagramDrawsRepository
from repositories.instagram_spider_accounts_repository import InstagramSpiderAccountsRepository
from repositories.instagram_tagging_accounts_repository import InstagramTaggingAccountsRepository
from repositories.session_decorator import close_session
from request.response import Response, InstagramDetailedResponse
from spiders.spider import Spider


def _query_instagram_spider_accounts(crawling):
    try:
        spider_account_id = crawling['data']['spider_account_id']
        spider_account = InstagramSpiderAccountsRepository().get_specific_spider_account(spider_account_id)
        if spider_account.is_banned:
            raise BannedSpiderException(spider_account.id)
    except KeyError:
        logger.info('Returning least used spider account since desired spider doesn\'t exists or it\'s banned')
        return InstagramSpiderAccountsRepository().get_least_used_active_spider_account()


def _get_random_active_draw():
    active_draws = InstagramDrawsRepository().get_active_draws()
    if len(active_draws) == 0:
        raise NoneActiveDrawsException()

    return active_draws[random.randint(0, len(active_draws) - 1)]


class InstagramSpider(Spider):
    def __init__(self, spider_name):
        super(InstagramSpider, self).__init__(spider_name)
        self.draw = None
        self.spider_account = None
        self.tagging_accounts = None
        self.tagging_count = None
        self.tagging_percentage = None
        self.following = False
        self.liked = False

    def prepare_spider(self, crawling):
        self.draw = _get_random_active_draw()
        self.spider_account = _query_instagram_spider_accounts(crawling)
        self.tagging_accounts = InstagramTaggingAccountsRepository().get_least_used_tagging_account_group()

    def process_task(self, crawling, web_driver_pool):
        driver = web_driver_pool.acquire(None, self._config.webdriver)
        # Go to instagram website
        driver.get(self._config.base_url)

        # Waiting for login page to be fully loaded
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, self._config.html_location.username_input)))
        logger.info('Logging user %s', self.spider_account.username)
        self._login(driver)

        # Waiting for user to be fully logged in and redirecting to
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, self._config.html_location.user_avatar)))
        driver.get("{}{}".format(self._config.base_url, self.draw.draw_url))
        logger.info('Participating in draw %s of account %s with deadline %s',
                    self.draw.draw_url, self.draw.draw_account, self.draw.expiry_date)

        tagging_response = None
        if self.draw.needs_tagging:
            try:
                tagging_response = self._tag_friends(driver)
            except Exception as ex:
                self.take_screenshot(driver, 'unexpected_exception')
                self._update_spider_last_time_used()
                self._update_selected_tagging_accounts_last_time_used()

                tagging_response = Response(str(ex), 500)

        like_response = None
        if self.draw.needs_like:
            try:
                like_response = self._like_post(driver)
            except Exception as ex:
                like_response = Response(str(ex), 500)

        follow_response = None
        if self.draw.needs_follow:
            try:
                follow_response = self._follow_accounts(driver)
            except Exception as ex:
                follow_response = Response(str(ex), 500)

        if self.draw.needs_post_story:
            self._post_to_story(driver)

        self._save_instagram_record(self.tagging_count, self.tagging_percentage)
        return InstagramDetailedResponse(tagging_response, follow_response, like_response, 200)

    def _login(self, driver):
        login_data = self.complete_login_data(driver)
        login_data.submit()
        try:
            driver.find_element_by_id("slfErrorAlert")
            logger.error("Will take a nap for 30 sec and try again. Hope it works")
            time.sleep(30)
            login_data = self.complete_login_data(driver)
            login_data.submit()
        except NoSuchElementException:
            pass

    def complete_login_data(self, driver):
        username_input = driver.find_element_by_xpath(self._config.html_location.username_input)
        username_input.send_keys(self.spider_account.username)
        password_input = driver.find_element_by_xpath(self._config.html_location.password_input)
        password_input.send_keys(self.spider_account.password)

        return password_input

    def _tag_friends(self, driver):
        subset_count = 0
        combinations_array = create_tags_combinations(self.tagging_accounts[1].split(','), self.draw.tags_needed)

        # Once we got here, we need to update spider_account and tagging_group last time used so we renew them each time
        self._update_spider_last_time_used()
        self._update_selected_tagging_accounts_last_time_used()

        for subset in combinations_array:
            comment_button = driver.find_element_by_xpath(self._config.html_location.comment_button)
            comment_button.click()
            # driver.find_element_by_xpath(self._config.html_location.text_area).click()
            comment_area = driver.switch_to.active_element
            comment_area.send_keys(' '.join(subset))
            time.sleep(3)
            comment_area.send_keys(" ")

            if self.draw.needs_message:
                comment_area.send_keys(self.draw.message)

            post_button = driver.find_element_by_xpath(self._config.html_location.submit_button)
            post_button.click()
            time.sleep(1.5)

            try:
                driver.find_element_by_xpath(self._config.html_location.blocked_banner)
                self._save_traces_into_computer(driver.page_source, 'blocked_banner')
                logger.error('Last element unable to be posted was -> %s', subset)
                logger.error('Total number of posted elements %s and %s posting percentage accuracy',
                             self.tagging_count, self.tagging_percentage)

                return Response('Tagging procedure ended up with ERRORS!', 429)
            except NoSuchElementException:
                subset_count += 1
                logger.info('Successfully commented %s/%s with tags %s and message %s',
                            subset_count, len(combinations_array), subset, self.draw.message)
                # Waiting for comment to be published
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, self._config.html_location.text_area)))

                time.sleep(45.5)
            except Exception:
                logger.error('An unexpected error occurred while tagging. Saving screenshot and html')
                self._save_traces_into_computer(driver, 'unexpected_exception')
                return Response('Tagging procedure ended up with ERRORS!', 429)
            finally:
                self.tagging_count = '{}/{}'.format(subset_count, len(combinations_array))
                self.tagging_percentage = subset_count * 100 / len(combinations_array)

        return Response('Successfully ended tagging procedure', 200)

    def _follow_accounts(self, driver):
        accounts_to_follow = self.draw.accounts_to_follow.replace('@', '').split(',')
        follow_status = [False] * len(accounts_to_follow)

        for index, account in enumerate(accounts_to_follow):
            driver.get('{}{}/'.format(self._config.base_url, account))
            try:
                follow_button = driver.find_element_by_xpath(self._config.html_location.follow_button)
                follow_button.click()
                logger.info('Successfully following account %s', account)
                follow_status[index] = True
            except NoSuchElementException:
                logger.info('Unable to locate follow button. Searching if already following account')
                try:
                    driver.find_element_by_xpath(self._config.html_location.unfollow_button)
                    logger.info('Successfully following account %s', account)
                    follow_status[index] = True
                except NoSuchElementException:
                    message = 'Unable to locate follow/following button for account {}'.format(account)
                    logger.error(message)
                    pass

        self.following = all(follow_status)
        return Response(
            'Successfully following all accounts' if self.following else 'Unable to follow some accounts',
            200 if self.following else 429)

    def _like_post(self, driver):
        try:
            like_state = driver.find_element_by_xpath(self._config.html_location.like_state).get_attribute('aria-label')
            if like_state == 'Like' or like_state == 'Me gusta':
                like_button = driver.find_element_by_xpath(self._config.html_location.like_button)  # Like button
                like_button.click()
                logger.info('Successfully liked the post')
                self.liked = True
            elif like_state == 'Unlike' or like_state == 'Ya no me gusta':
                logger.info('Already liked post')
                self.liked = True
            else:
                logger.error("No idea what could be going on in here")
                return Response('Unable to like post', 404)
        except NoSuchElementException:
            logger.error('Unable to locate like button')
            return Response('Unable to like post', 404)

        return Response('Successfully liked post', 200)

    def _post_to_story(self, driver):
        # share_button = driver.find_element_by_xpath('//button[@class="wpO6b  "]')
        # share_button.click()
        # WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, './/div[@aria-label="Compartir"]')))
        # TODO: Here we should click the option that publishes this to our own story. After doing that, we should tag the account

        pass  # THIS OPTION IS NOT YET AVAILABLE!

    def _save_html(self, html_content):
        draw_info = 'drawId:{}.spiderId:{}'.format(self.draw.id, self.spider_account.id)
        self.save_html(html_content, [draw_info])

    def _save_traces_into_computer(self, driver, message):
        self._save_html(driver.page_source)
        self.take_screenshot(driver, message)

    @close_session
    def _save_instagram_record(self, tagging_count, percentage):
        logger.info('Saving crawling result into InstagramCrawling table')
        instagram_crawling_repository = InstagramCrawlingRepository()
        instagram_crawling_repository \
            .add_record(self.spider_account.id, self.draw.id, self.tagging_accounts.group_id, tagging_count, percentage,
                        self.draw.tags_needed, self.following, self.liked)

        return instagram_crawling_repository

    @close_session
    def _update_spider_last_time_used(self):
        instagram_spider_accounts_repository = InstagramSpiderAccountsRepository()
        instagram_spider_accounts_repository.update_spider_last_time_used(self.spider_account.id)

        return instagram_spider_accounts_repository

    @close_session
    def _update_selected_tagging_accounts_last_time_used(self):
        instagram_tagging_accounts_repository = InstagramTaggingAccountsRepository()
        instagram_tagging_accounts_repository \
            .update_selected_tagging_accounts_last_time_used(self.tagging_accounts.group_id)

        return instagram_tagging_accounts_repository
