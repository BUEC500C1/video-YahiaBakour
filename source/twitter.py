import tweepy
from config import TWITTER_API_KEY , TWITTER_API_SECRET_KEY , TWITTER_ACCESS_TOKEN , TWITTER_ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

class Tweet():
    def __init__(self, name, text, profilePic, images):
        self.name = name
        self.text = text
        self.images = images
        self.profilePic = profilePic
    
    def json(self):
        return {"name": self.name, "text": self.text, "images": self.images, 'profilePic':self.profilePic}
        
        
class Twitter():
    def __init__(self,user):
        self.feed = [self.extractInfo(tweet).json() for tweet in self.getTweets(user)]
        
    def getTweets(self,user):
        return api.user_timeline(user,include_entities=True)

    def extractInfo(self,tweet):
        text = tweet.text
        name = tweet.user.screen_name
        images = []
        profilePic = tweet.user.profile_image_url.replace('_normal', '')
        if 'media' in tweet.entities:
            for image in  tweet.entities['media']:
                if (image['type'] == 'photo'):
                    images.append(image['media_url'])
        return Tweet(name,text,profilePic,images)


