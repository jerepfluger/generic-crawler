from sqlalchemy import Column, String, Integer, Boolean

from base import Base


class InstagramSpiderAccounts(Base):
    __tablename__ = 'instagram_spider_accounts'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    is_banned = Column(Boolean)
