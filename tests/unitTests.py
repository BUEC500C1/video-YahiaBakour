import sys, os
import unittest
sys.path.insert(1, './source/')
from twitter import Twitter
from api import app
from resources import convert_images_to_video, createThreadsForProducingImages
import os

class APPTESTS(unittest.TestCase):
    def test_twitter(self):
        tweets = Twitter("Reuters").feed
        assert tweets != []
        assert tweets is not None

    def test_get(self):
        client = app.test_client()
        data = client.get('/user?twittername=Reuters')
        assert data._status_code == 200

    def test_sample_video_creation(self):
        videoName = "unitTest"
        response = convert_images_to_video(os.getcwd()+ "/images_created/sample/elonmusk",videoName)
        assert response == True
        assert os.path.isfile(f'{os.getcwd()}/source/static/video_generated/{videoName}.ogg') == True

    def test_thread_creation_for_image_production(self):
        tweets = Twitter("Reuters").feed
        threads = createThreadsForProducingImages(tweets,os.getcwd()+ "/images_created/sample/Reuters/")
        assert threads != []
unittest.main()