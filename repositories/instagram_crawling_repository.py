from repositories.entities.instagram_crawling_entity import InstagramCrawling

from base import Session, engine, Base

Base.metadata.create_all(engine)


class InstagramCrawlingRepository:
    def __init__(self):
        self.session = Session()

    def add_record(self, draw, account_draw, tagging_count, tagging_percentage, tags_needed, followed, liked):
        instagram_crawling = InstagramCrawling(draw, account_draw, tagging_count, tagging_percentage,
                                               tags_needed, followed, liked)
        self.session.add(instagram_crawling)
        self.session.commit()
        self.session.close()
