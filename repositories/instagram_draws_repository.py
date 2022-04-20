from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.sql.expression import false

from base import Session, engine, Base
from repositories.entities.instagram_draws import InstagramDraws

Base.metadata.create_all(engine)


class InstagramDrawsRepository:
    def __init__(self):
        self.session = Session()

    def get_active_draws(self):
        now = datetime.now()
        return self.session.query(InstagramDraws) \
            .filter(
            and_(
                InstagramDraws.expiry_date > now,
                InstagramDraws.expired == false()
            )) \
            .all()
