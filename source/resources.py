
from flask_restful import Resource, Api
from twitter import Twitter
from webargs import fields
from webargs.flaskparser import use_args
import os
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import threading
import time

def createLocalDir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    return True

    

def generateImage(name,text,imageIdx,path):
    # copying image to another image object 
    im1 = Image.open('background.png')
    image = im1.copy() 
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', size=12)
    (x, y) = (50, 50)
    message = text
    wrapped = wrap(message,100)
    message = "\n".join(wrapped)
    color = 'rgb(0, 0, 0)' 
    draw.text((x, y), message, fill=color, font=font)
    (x, y) = (150, 150)
    color = 'rgb(255, 255, 255)' # white color
    draw.text((x, y), name, fill=color, font=font)
    image.save(path+str(imageIdx)+'.png')
    return True

class TwitterFeedSummarize(Resource):
    @use_args({"twittername": fields.Str(required=True)})
    def get(self,args):
        twitterObj = Twitter(args['twittername'])
        feed = twitterObj.feed
        result = []
        threads = []
        imageIdx =0 
        path = os.getcwd()+ "/images_created"
        createLocalDir(path)
        path = path + '/' + args['twittername'] + '/'
        createLocalDir(path)
        
        for tweet in feed:
            imageForTweet = []
            # for image in tweet['images']:
            #     imageData = getImageDescription(image)
            #     imageForTweet.append({ 'objects':imageData.objects })
            result.append({
                'name' : tweet['name'],
                'text' : tweet['text'],
            })
            threads.append(threading.Thread(target=generateImage, args=(tweet['name'],tweet['text'],imageIdx,path)))
            imageIdx+=1
        for thread in threads:
            thread.start()

        return result