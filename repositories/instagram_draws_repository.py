from base import Session, engine, Base

Base.metadata.create_all(engine)


class InstagramDrawsRepository:
    def __init__(self):
        self.session = Session()

    def add_new_instagram_draw(self):
        pass
