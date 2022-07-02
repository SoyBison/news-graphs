from flask import Flask, render_template, make_response
import pandas as pd
from flask_restful import Resource, Api
from dotenv import load_dotenv
from src.data import ENGINE

app = Flask(__name__)
api = Api(app)
load_dotenv()


class NewsStream(Resource):
    @staticmethod
    def get():
        transitory_df = pd.read_sql("SELECT * FROM articles", con=ENGINE)
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
