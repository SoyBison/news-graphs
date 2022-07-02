import os
import requests
import pandas as pd
import json
from sqlalchemy import create_engine
from .data import setup

eng_url = os.getenv("DATABASE_URL")
ENGINE = create_engine(eng_url, echo=False)


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
    pubtimes = map(lambda d: d["publishedAt"], articles)
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
    transitory_df.to_sql("temp_articles", con=ENGINE, index=False, if_exists="replace")

    with ENGINE.begin() as cn:
        sql = """
            INSERT INTO articles (source_id, author, url, timestamp, source, title, description, url_to_image)
            SELECT t.source_id, t.author, t.url, t.timestamp, t.source, t.title, t.description, t.url_to_image
            FROM temp_articles t
            WHERE NOT EXISTS
                (SELECT 1 FROM articles f
                 WHERE t.url = f.url)
        """
        cn.execute(sql)


if __name__ == '__main__':
    setup()
    record()
