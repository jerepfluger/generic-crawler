from datetime import datetime

from sqlalchemy import asc, func

from base import Session, engine, Base
from repositories.entities.instagram_tagging_accounts import InstagramTaggingAccounts

Base.metadata.create_all(engine)


class InstagramTaggingAccountsRepository:
    def __init__(self):
        self.session = Session()

    def get_least_used_tagging_account_group(self):
        least_used_group = self._get_least_used_group_id()

        return self.session.query(InstagramTaggingAccounts.group_id,
                                  func.group_concat(InstagramTaggingAccounts.account)) \
            .filter(InstagramTaggingAccounts.group_id == least_used_group.group_id) \
            .group_by(InstagramTaggingAccounts.group_id) \
            .one()

    def get_tagging_accounts_groups(self):
        return self.session.query(InstagramTaggingAccounts.group_id,
                                  func.group_concat(InstagramTaggingAccounts.account)) \
            .group_by(InstagramTaggingAccounts.group_id).all()

    def _get_least_used_group_id(self):
        return self.session.query(InstagramTaggingAccounts) \
            .order_by(asc(InstagramTaggingAccounts.last_used)) \
            .first()

    def update_selected_tagging_accounts_last_time_used(self, group_id):
        timestamp = datetime.now().strftime('%Y:%m:%d %H:%m:%S')
        self.session.query(InstagramTaggingAccounts) \
            .filter(InstagramTaggingAccounts.group_id == group_id) \
            .update({InstagramTaggingAccounts.last_used: timestamp})

        self.session.commit()

    def close_session(self):
        self.session.close()
