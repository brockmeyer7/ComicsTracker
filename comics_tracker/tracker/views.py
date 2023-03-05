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
def book(request, title: str, start_year: int, iss_start_num: int, iss_end_num: int):
    if request.method == 'GET':
        result = []
        api_response = json.loads(book_lookup(title, start_year, iss_start_num, iss_end_num))
        for item in api_response:
            item_dict = {}
            item_dict['id'] = item['data']['results'][0]['id']
            item_dict['issue_num'] = item['data']['results'][0]['issueNumber']
            item_dict['title'] = item['data']['results'][0]['title']
            item_dict['description'] = item['data']['results'][0]['description']
            result.append(item_dict)
        return HttpResponse(json.dumps(result))


@require_http_methods(['GET'])
def character(request, name: str):
    if request.method == 'GET':
        result = {}
        api_response = json.loads(character_lookup(name))['data']['results'][0]
        result['id'] = api_response['id']
        result['name'] = api_response['name']
        result['description'] = api_response['description']
        return HttpResponse(json.dumps(result))

def character_lookup(name: str):
    auth_string = api_auth()
    api_url = 'https://gateway.marvel.com:443/v1/public/characters?name=' + name + '&' + auth_string
    response = requests.get(api_url)
    return json.dumps(response.json())

def book_lookup(title: str, start_year: int, iss_start_num: int, iss_end_num: int):
    auth_string = api_auth()
    api_url = 'https://gateway.marvel.com:443/v1/public/comics?' + auth_string + '&title=' + title + '&startYear=' + str(start_year)
    result = []
    for i in range(iss_start_num, iss_end_num + 1):
        response = requests.get(api_url + '&issueNumber=' + str(i))
        result.append(response.json())
    return json.dumps(result)       

def api_auth():
    dotenv_path = os.path.expanduser('~/Documents/Personal_Projects/.env')
    load_dotenv(dotenv_path)
    public_key = os.getenv('MARVEL_PUBLIC_KEY')
    private_key = os.getenv('MARVEL_PRIVATE_KEY')
    gmt = time.gmtime()
    ts = str(calendar.timegm(gmt))
    hash = hashlib.md5((ts+private_key+public_key).encode())
    return ('ts=' + ts + '&apikey=' + public_key + '&hash=' + hash.hexdigest())