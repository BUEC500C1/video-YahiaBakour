from flask import Flask
from flask_restful import Resource, Api
from resources import TwitterFeedSummarize

app = Flask(__name__)
api = Api(app)

api.add_resource(TwitterFeedSummarize, '/user')

if __name__ == '__main__':
    app.run(debug=True)
