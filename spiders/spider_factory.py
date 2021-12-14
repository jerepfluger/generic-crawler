from spiders.instagram_spider import InstagramSpider
from spiders.twitter_spider import TwitterSpider


class SpiderFactory:
    spiders = {
        'twitter': TwitterSpider('twitter'),
        'instagram': InstagramSpider('instagram')
    }

    @staticmethod
    def choose(spider_name):
        return SpiderFactory.spiders.get(spider_name, Exception("There's no spider implementation for {}".format(spider_name)))
