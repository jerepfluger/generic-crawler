from sqlalchemy import Column, Integer

from base import Base


class InstagramTaggingAccounts(Base):
    __tablename__ = 'instagram_tagging_accounts'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    account = Column(Integer)
