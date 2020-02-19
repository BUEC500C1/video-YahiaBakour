from flask import Flask, redirect
from flask_restful import Resource, Api
from resources import TwitterFeedVideoMaker

app = Flask(__name__)
api = Api(app)

api.add_resource(TwitterFeedVideoMaker, '/user')


@app.route('/video/<name>')
def watchVideo(name):
    return redirect('../static/video_generated/'+name)

if __name__ == '__main__':
    app.run(debug=True)
