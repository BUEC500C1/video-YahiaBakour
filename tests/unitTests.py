import sys, os
import unittest
sys.path.insert(1, './source/')
from twitter import Twitter
from api import app


class APPTESTS(unittest.TestCase):
    def test_twitter(self):
        tweets = Twitter("Reuters").feed
        assert tweets != []
        assert tweets is not None


    def test_get(self):
        client = app.test_client()
        data = client.get('/user?twittername=Reuters')
        assert data._status_code == 200
        
if __name__ == '__main__':
    unittest.main()