from sqlalchemy import Column, String, Integer, Boolean, Float, TIMESTAMP, ForeignKey

from base import Base


class InstagramCrawling(Base):
    __tablename__ = 'instagram_crawling'

    id = Column(Integer, primary_key=True)
    crawling_timestamp = Column(TIMESTAMP)
    spider_account_id = Column(Integer, ForeignKey('instagram_spider_accounts.id'))
    draw_id = Column(String, ForeignKey('instagram_draws.id'))
    tagging_group_id = Column(Integer, ForeignKey('instagram_tagging_accounts.group_id'))
    tagging_count = Column(String)
    tagging_percentage = Column(Float)
    tags_needed = Column(Integer)
    followed = Column(Boolean)
    liked = Column(Boolean)

    def __init__(self, crawling_timestamp, spider_account, draw_id, tagging_group_id,
                 tagging_count, tagging_percentage, tags_needed, followed, liked):
        self.crawling_timestamp = crawling_timestamp
        self.spider_account_id = spider_account
        self.draw_id = draw_id
        self.tagging_group_id = tagging_group_id
        self.tagging_count = tagging_count
        self.tagging_percentage = tagging_percentage
        self.tags_needed = tags_needed
        self.followed = followed
        self.liked = liked
