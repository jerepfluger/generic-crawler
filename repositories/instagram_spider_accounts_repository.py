from datetime import datetime

from sqlalchemy import asc
from sqlalchemy.sql.expression import false

from base import Session, engine, Base
from repositories.entities.instagram_spider_accounts import InstagramSpiderAccounts

Base.metadata.create_all(engine)


class InstagramSpiderAccountsRepository:
    def __init__(self):
        self.session = Session()

    def get_least_used_active_spider_account(self):
        spider_account = self.session.query(InstagramSpiderAccounts) \
            .filter(InstagramSpiderAccounts.is_banned == false()) \
            .order_by(asc(InstagramSpiderAccounts.last_used)) \
            .one()
        self.update_spider_last_used(spider_account.id)

        return spider_account

    def get_active_spider_accounts(self):
        return self.session.query(InstagramSpiderAccounts).filter(InstagramSpiderAccounts.is_banned == false()).all()

    def get_specific_spider_account(self, spider_account_id):
        return self.session.query(InstagramSpiderAccounts).filter(InstagramSpiderAccounts.id == spider_account_id).all()

    def update_spider_last_used(self, spider_id):
        timestamp = datetime.now().strftime('%Y:%m:%d %H:%m:%S')
        self.session.query(InstagramSpiderAccounts).filter(InstagramSpiderAccounts.id == spider_id).update(
            {InstagramSpiderAccounts.last_used: timestamp})
