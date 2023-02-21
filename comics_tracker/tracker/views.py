from django.shortcuts import render
from django.http import HttpResponse
import hashlib
import calendar, time
import requests, json
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

def index(request):
    result = []
    threads=[]
    with ThreadPoolExecutor(max_workers=20) as executor:
        for i in range(20):
            threads.append(executor.submit(character_lookup, i * 100))
            
        for task in as_completed(threads):
            for item in json.loads(task.result())['data']['results']:
                result.append(item['name'])
    return HttpResponse(json.dumps(result))

def character_lookup(offset):
    auth_string = api_auth()
    api_url = 'https://gateway.marvel.com:443/v1/public/characters?limit=100&offset=' + str(offset) + '&' + auth_string
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
    return ('ts=' + ts + '&apikey=' + public_key + '&hash=' + hash.hexdigest())