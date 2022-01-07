from datetime import datetime

from base import Session, engine, Base
from repositories.entities.instagram_draws import InstagramDraws

Base.metadata.create_all(engine)


class InstagramDrawsRepository:
    def __init__(self):
        self.session = Session()

    def get_active_draws(self):
        now = datetime.now()
        return self.session.query(InstagramDraws).filter(InstagramDraws.expiry_date > now).all()

    def close_session(self):
        self.session.close()
