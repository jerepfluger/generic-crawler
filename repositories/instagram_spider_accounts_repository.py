from base import Session, engine, Base

Base.metadata.create_all(engine)


class InstagramSpiderAccounts:
    def __init__(self):
        self.session = Session()

    def add_new_spider_account(self):
        pass
