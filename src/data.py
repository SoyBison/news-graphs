from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()
eng_url = os.getenv("DATABASE_URL")
ENGINE = create_engine(eng_url, echo=False)


class Article(Base):
    __tablename__ = 'articles'
    uri = Column(String, primary_key=True)
    byline = Column(String)
    timestamp = Column(DateTime)
    title = Column(String)
    abstract = Column(String)
    section = Column(String)
    subsection = Column(String)
    material_type = Column(String)
    url = Column(String)
    des_facet = Column(String)
    per_facet = Column(String)
    geo_facet = Column(String)
    org_facet = Column(String)


def setup():
    Base.metadata.create_all(ENGINE, checkfirst=True)
