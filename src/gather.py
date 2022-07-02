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
    news_string = "https://api.nytimes.com/svc/news/v3/content/all/all.json"
    key = os.getenv("NEWS_API_KEY")
    key_string = "?api-key=" + key
    r = requests.get(news_string + key_string)
    data = json.loads(r.text)
    articles = data['results']
    bylines = map(lambda d: d["byline"], articles)
    urls = map(lambda d: d["url"], articles)
    uris = map(lambda d: d["uri"], articles)  # I think these are uuids, which is pretty cool NYT
    pubtimes = map(lambda d: pd.Timestamp(d["published_date"]), articles)
    sections = map(lambda d: d["section"], articles)
    subsections = map(lambda d: d["subsection"], articles)
    material_type = map(lambda d: d["material_type_facet"], articles)
    titles = map(lambda d: d["title"], articles)
    descs = map(lambda d: d["abstract"], articles)
    # Facets are interesting, looks like it's a way for them to internally organize topics?
    # Too bad they violate SQL Norms, but a little json never hurt nobody.
    des_facet = map(lambda d: json.dumps(d["des_facet"]), articles)
    org_facet = map(lambda d: json.dumps(d["org_facet"]), articles)
    per_facet = map(lambda d: json.dumps(d["per_facet"]), articles)
    geo_facet = map(lambda d: json.dumps(d["geo_facet"]), articles)

    transitory_df = pd.DataFrame({
        "byline": bylines,
        "url": urls,
        "uri": uris,
        "timestamp": pubtimes,
        "title": titles,
        "abstract": descs,
        "section": sections,
        "subsection": subsections,
        "material_type": material_type,
        "des_facet": des_facet,
        "per_facet": per_facet,
        "org_facet": org_facet,
        "geo_facet": geo_facet,
    })
    existing_urls = pd.read_sql("SELECT uri FROM articles", con=ENGINE)
    good_uris = set(transitory_df['uri']) - set(existing_urls['uri'])
    transitory_df = transitory_df[transitory_df['uri'].isin(good_uris)]
    transitory_df.to_sql("articles", con=ENGINE, index=False, if_exists="append")


if __name__ == '__main__':
    setup()
    record()
