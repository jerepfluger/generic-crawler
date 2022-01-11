from datetime import datetime

from base import Session, engine, Base
from repositories.entities.instagram_crawling import InstagramCrawling

Base.metadata.create_all(engine)


class InstagramCrawlingRepository:
    def __init__(self):
        self.session = Session()

    def add_record(self, spider_account_id, draw_id, tagging_group_id, tagging_count, tagging_percentage,
                   tags_needed, followed, liked):
        timestamp = datetime.now().strftime('%Y:%m:%d %H:%m:%S')
        instagram_crawling = InstagramCrawling(timestamp, spider_account_id, draw_id, tagging_group_id,
                                               tagging_count, tagging_percentage, tags_needed, followed, liked)
        self.session.add(instagram_crawling)
        self.session.commit()

    def get_crawling_by_draw_id(self, draw_id):
        self.session.query(InstagramCrawling) \
            .filter(InstagramCrawling.draw_id == draw_id) \
            .all()

    def close_session(self):
        self.session.close()
