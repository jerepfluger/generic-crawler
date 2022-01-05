from base import Session, engine, Base

Base.metadata.create_all(engine)


class InstagramTaggingAccounts:
    def __init__(self):
        self.session = Session()

    def add_new_tagging_account(self):
        pass
