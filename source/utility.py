import requests

def getImage(url):
    return requests.get(url, stream=True).content
