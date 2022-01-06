from sqlalchemy import func

from base import Session, engine, Base
from repositories.entities.instagram_tagging_accounts import InstagramTaggingAccounts

Base.metadata.create_all(engine)


class InstagramTaggingAccountsRepository:
    def __init__(self):
        self.session = Session()

    def get_tagging_accounts_groups(self):
        return self.session.query(InstagramTaggingAccounts.group_id,
                                  func.group_concat(InstagramTaggingAccounts.account)) \
            .group_by(InstagramTaggingAccounts.group_id).all()
