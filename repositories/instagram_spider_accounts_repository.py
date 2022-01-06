from sqlalchemy.sql.expression import false

from base import Session, engine, Base
from repositories.entities.instagram_spider_accounts import InstagramSpiderAccounts

Base.metadata.create_all(engine)


class InstagramSpiderAccountsRepository:
    def __init__(self):
        self.session = Session()

    def get_active_spider_accounts(self):
        return self.session.query(InstagramSpiderAccounts).filter(InstagramSpiderAccounts.is_banned == false()).all()

    def get_specific_spider_account(self, spider_account_id):
        return self.session.query(InstagramSpiderAccounts).filter(InstagramSpiderAccounts.id == spider_account_id).all()
