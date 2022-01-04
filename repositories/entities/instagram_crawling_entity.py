from sqlalchemy import Column, String, Integer, Boolean, Float
from base import Base


class InstagramCrawling(Base):
    __tablename__ = 'instagram_crawling'

    id = Column(Integer, primary_key=True)
    draw = Column(String)
    account_draw = Column(String)
    tagging_count = Column(String)
    tagging_percentage = Column(Float)
    tags_needed = Column(Integer)
    followed = Column(Boolean)
    liked = Column(Boolean)

    def __init__(self, draw, account_draw, tagging_count, tagging_percentage, tags_needed, followed, liked):
        self.draw = draw
        self.account_draw = account_draw
        self.tagging_count = tagging_count
        self.tagging_percentage = tagging_percentage
        self.tags_needed = tags_needed
        self.followed = followed
        self.liked = liked
