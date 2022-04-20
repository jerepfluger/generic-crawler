from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP

from base import Base


class InstagramDraws(Base):
    __tablename__ = 'instagram_draws'

    id = Column(Integer, primary_key=True)
    draw_url = Column(String)
    draw_account = Column(String)
    needs_tagging = Column(Boolean)
    tags_needed = Column(Integer)
    needs_message = Column(Boolean)
    message = Column(String)
    needs_post_story = Column(Boolean)
    needs_like = Column(Boolean)
    needs_follow = Column(Boolean)
    accounts_to_follow = Column(String)
    expiry_date = Column(TIMESTAMP)
    expired = Column(Boolean)
    won = Column(Boolean)
    extra_info = Column(String)
