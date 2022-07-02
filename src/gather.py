import os
import numpy as np
import requests
import pandas as pd
import json
from sqlalchemy import create_engine, MetaData
from data import setup
import datetime

eng_url = os.getenv("DATABASE_URL")
ENGINE = create_engine(eng_url, echo=False)
META = MetaData()
META.reflect(ENGINE)


def record():
    news_string = "https://newsapi.org/v2/top-headlines?country=us"
    key = os.getenv("NEWS_API_KEY")
    key_string = "&apiKey=" + key
    r = requests.get(news_string + key_string)
    data = json.loads(r.text)
    articles = data['articles']
    source_ids = map(lambda d: d['source']['id'], articles)
    bylines = map(lambda d: d["author"], articles)
    urls = map(lambda d: d["url"], articles)
    pubtimes = map(lambda d: pd.Timestamp(d["publishedAt"]), articles)
    sources = map(lambda d: d["source"]['name'], articles)
    titles = map(lambda d: d["title"], articles)
    descs = map(lambda d: d["description"], articles)
    imgs = map(lambda d: d["urlToImage"], articles)
    transitory_df = pd.DataFrame({
        "source_id": source_ids,
        "author": bylines,
        "url": urls,
        "timestamp": pubtimes,
        "source": sources,
        "title": titles,
        "description": descs,
        "url_to_image": imgs,
    })
    existing_urls = pd.read_sql("SELECT url FROM articles", con=ENGINE)
    transitory_df = transitory_df[np.isin(transitory_df["url"], set(existing_urls["url"].unique()))]
    transitory_df.to_sql("articles", con=ENGINE, index=False, if_exists="append")


def prune():
    too_old = datetime.datetime.now() - datetime.timedelta(days=28)
    for table in META.sorted_tables:
        ENGINE.execute(table.delete().where(table.c.timestamp <= too_old))


if __name__ == '__main__':
    setup()
    record()
    prune()
