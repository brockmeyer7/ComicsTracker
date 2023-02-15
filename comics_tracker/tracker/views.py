from django.shortcuts import render
from django.http import HttpResponse
import hashlib
import calendar, time
import requests, json
import os
from dotenv import load_dotenv

def index(request):
    response = json.loads(str(character_lookup()))
    result = []
    for item in response['data']['results']:
        result.append(item['name'])
    return HttpResponse(json.dumps(result))

def character_lookup():
    ts, public_key, hash = api_auth()
    api_url = 'https://gateway.marvel.com:443/v1/public/characters?ts=' + ts + '&apikey=' + public_key + '&hash=' + hash.hexdigest()
    response = requests.get(api_url)
    return json.dumps(response.json())

def api_auth():
    dotenv_path = os.path.expanduser('~/Documents/Personal_Projects/.env')
    load_dotenv(dotenv_path)
    public_key = os.getenv('MARVEL_PUBLIC_KEY')
    private_key = os.getenv('MARVEL_PRIVATE_KEY')
    gmt = time.gmtime()
    ts = str(calendar.timegm(gmt))
    hash = hashlib.md5((ts+private_key+public_key).encode())
    return ts, public_key, hash

