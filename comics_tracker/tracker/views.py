from django.shortcuts import render
from django.http import HttpResponse
import hashlib
import calendar, time
import requests, json
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.views.decorators.http import require_http_methods

def index(request):
    return HttpResponse("Hello World!")

@require_http_methods(['GET'])
def book(request):
    if request.method == 'GET':
        pass

@require_http_methods(['GET'])
def character(request, name: str):
    if request.method == 'GET':
        result = {}
        api_response = json.loads(character_lookup(name))
        print(api_response['data']['results'][0]['name'])
        # result['id'] = api_response['data']['results']['id']
        # result['name'] = api_response['data']['results']['name']
        # result['description'] = api_response['data']['results']['description']
        return HttpResponse(character_lookup(name))

def character_lookup(name: str):
    auth_string = api_auth()
    api_url = 'https://gateway.marvel.com:443/v1/public/characters?name=' + name + '&' + auth_string
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