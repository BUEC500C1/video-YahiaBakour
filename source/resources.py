
from flask_restful import Resource, Api
from twitter import Twitter
from webargs import fields
from webargs.flaskparser import use_args

class TwitterFeedSummarize(Resource):
    @use_args({"twittername": fields.Str(required=True)})
    def get(self,args):
        twitterObj = Twitter(args['twittername'])
        feed = twitterObj.feed
        result = []
        for tweet in feed:
            imageForTweet = []
            # for image in tweet['images']:
            #     imageData = getImageDescription(image)
            #     imageForTweet.append({ 'objects':imageData.objects })
            result.append({
                'name' : tweet['name'],
                'text' : tweet['text'],
            })
        return result