from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: This needs to be set by config
engine = create_engine('mysql://root:J3r3mia$123@localhost:3306/generic_crawler')
Session = sessionmaker(bind=engine)

Base = declarative_base()
