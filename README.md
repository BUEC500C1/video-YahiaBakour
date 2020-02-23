# Yahia Bakour FFMPEG Twitter Video Creator

HW3 for EC500.

By: Yahia Bakour

Email: yehia234@bu.edu

BUID: U37575373

## Getting Started

#### To setup server

```
python3 app.py
```

#### To get data from server

```
curl http://0.0.0.0:8000/user\?twittername\=Reuters
```

## Background Info
- When the /user endpoint is hit, i produce a hash to identify the end video created and immediately return it, in the meantime i spawn a thread that goes to work and creates the images then video
- All images are created in parallel with as many threads as needed 
- Immediately aggregate images to video
- if endpoint for viewing video is hit, then either return the video or return that the video isnt ready yet
- profit ???



### Prerequisites

You will need to setup your config source/config.py file as shown

```
TWITTER_API_KEY = XXXXXXXXX
TWITTER_API_SECRET_KEY = XXXXXXXXXXXXXXXXXX
TWITTER_ACCESS_TOKEN = XXXXXXXXX
TWITTER_ACCESS_TOKEN_SECRET = XXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Twitter Keys:

[Setup a Twitter API Key](https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/) - Twitter API Key how to




### Installing

Install requirements
```
pip3 install -r requirements.txt
```

## Running the tests

```
python3 tests/unitTests.py
```

## Results

running

```
curl http://0.0.0.0:8000/user\?twittername\=Reuters
```

Produces

```
{
  "videoURL": "http://127.0.0.1:5000/video/XYZ.ogg"
}
```


## Built With

* [Tweepy](http://docs.tweepy.org/en/latest/api.html) - Tweepy API
* [Flask Restful](https://flask-restful.readthedocs.io/en/latest/) - Flask Restful
* [FFMPEG](https://www.ffmpeg.org/) - FFMPEG

## Authors

* **Yahia Bakour** - [Website](https://yahiabakour.com/)
