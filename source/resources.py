
from flask_restful import Resource, Api
from twitter import Twitter
from webargs import fields
from webargs.flaskparser import use_args
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops
from textwrap import wrap
import threading
import time
from utility import getImage
from io import BytesIO
from subprocess import Popen
from multiprocessing import Queue, current_process

# queue stuff
work_queue = Queue()
def workDispatcher(process_pool):
    while True:
        videoId, userTwitterHandle  = work_queue.get()
        process_pool.apply_async(createVideo, args=(userTwitterHandle, videoId))

def addToQueue(videoId,TwitterHandle):
    work_queue.put((videoId,TwitterHandle))


# directory creation
def createLocalDir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("directory %s already exists" % path)
    else:
        print ("Successfully created the directory %s " % path)
    return True


def createNecessaryDirectories(twitterName,Hash):
    # create necessary directories
    createLocalDir(os.getcwd()+ "/source/static/")
    createLocalDir(os.getcwd()+ "/source/static/video_generated")
    path = os.getcwd()+ "/images_created"
    createLocalDir(path)
    path = path + '/' + Hash + '/'
    createLocalDir(path)
    path = path + '/' + twitterName + '/'
    createLocalDir(path)
    return path

# Taken From : https://stackoverflow.com/a/22336005
def makeCircular(crop_img):
    bigsize = (crop_img.size[0]*3, crop_img.size[1]*3)
    mask = Image.new('L', bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(crop_img.size, Image.ANTIALIAS)
    crop_img.putalpha(mask)
    return crop_img, mask

def generateImage(name,text,pic,imageIdx,path):
    # copying image to another image object 
    im1 = Image.open('background.png')
    image = im1.copy() 
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', size=16)
    (x, y) = (50, 50)
    color = 'rgb(255, 255, 255)' # white color

    # add message text and wrap if needed
    message = text
    wrapped = wrap(message,60)
    message = "\n".join(wrapped)
    draw.text((x, y), message, fill=color, font=font)

    # slap on name
    (x, y) = (450, 280)
    draw.text((x, y), '@'+name, fill=color, font=font)

    # slap on profile pic
    profilePicBytes = getImage(pic)
    user_photo = Image.open(BytesIO(profilePicBytes)).convert( 'RGBA' ).resize((110, 110))
    user_photo, mask = makeCircular(user_photo)
    image.paste(user_photo, (620,230), mask)

    image.save(path+"image"+str(imageIdx)+'.png')
    return True

def createThreadsForProducingImages(feed,path):
    threads = []
    imageIdx = 0
    for tweet in feed:
        threads.append(threading.Thread(target=generateImage, args=(tweet['name'],tweet['text'],tweet['profilePic'],imageIdx,path)))
        imageIdx+=1
    return threads

def convert_images_to_video(image_path, video_id):
    cmd = 'ffmpeg -r 1 -i '+image_path+'/image%d.png -preset ultrafast -r 1/3 -y ./source/static/video_generated/'+video_id+'.ogg'
    os.system(cmd)
    return True

def createVideo(twitterName,hashCreated):
    twitterObj = Twitter(twitterName)
    path = createNecessaryDirectories(twitterName,hashCreated)
    threads = createThreadsForProducingImages(twitterObj.feed,path)

    # start threads
    for thread in threads:
        thread.start()

    # join threads
    for thread in threads:
        thread.join()

    convert_images_to_video(path,hashCreated)

    return True