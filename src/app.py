from flask import Flask, render_template, make_response
import pandas as pd
from flask_restful import Resource, Api
import requests
from dotenv import load_dotenv
import json
import os

app = Flask(__name__)
api = Api(app)
load_dotenv()


class NewsStream(Resource):
    news_string = "https://newsapi.org/v2/top-headlines?country=us"
    key = os.getenv("NEWS_API_KEY")
    key_string = "&apiKey=" + key

    def get(self):
        r = requests.get(self.news_string + self.key_string)
        data = json.loads(r.text)
        articles = data['articles']
        source_ids = map(lambda d: d['source']['id'], articles)
        bylines = map(lambda d: d["author"], articles)
        urls = map(lambda d: d["url"], articles)
        pubtimes = map(lambda d: d["publishedAt"], articles)
        transitory_df = pd.DataFrame({
            "Source": source_ids,
            "By": bylines,
            "Url": urls,
            "Timestamp": pubtimes,
        })
        resp = make_response(transitory_df.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp


@app.route("/")
def hello():
    return render_template('index.html')


api.add_resource(NewsStream, "/data")

if __name__ == '__main__':
    app.run(debug=True)
