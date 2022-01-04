from datetime import datetime

from base import Session, engine, Base
from repositories.entities.instagram_crawling_entity import InstagramCrawling

Base.metadata.create_all(engine)


class InstagramCrawlingRepository:
    def __init__(self):
        self.session = Session()

    def add_record(self, draw, account_draw, tagging_count, tagging_percentage, tags_needed, followed, liked):
        timestamp = datetime.now().strftime("%Y:%m:%d %H:%m:%S")
        instagram_crawling = InstagramCrawling(timestamp, draw, account_draw, tagging_count, tagging_percentage,
                                               tags_needed, followed, liked)
        self.session.add(instagram_crawling)
        self.session.commit()
        self.session.close()
