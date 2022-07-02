from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()
eng_url = os.getenv("DATABASE_URL")
ENGINE = create_engine(eng_url, echo=False)


class Article(Base):
    __tablename__ = 'articles'
    url = Column(String, primary_key=True)
    author = Column(String)
    source_id = Column(String)
    source = Column(String)
    timestamp = Column(DateTime)
    title = Column(String)
    description = Column(String)
    url_to_image = Column(String)


def setup():
    Base.metadata.create_all(ENGINE, checkfirst=True)
