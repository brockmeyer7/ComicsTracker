from django.shortcuts import render
from django.http import HttpResponse
import hashlib
import calendar, time
import requests, json
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.views.decorators.http import require_http_methods
import mokkari

def index(request):
    return HttpResponse("Hello World!")

@require_http_methods(['GET'])
def book(request, series_name: str, series_year_began: int, iss_num_start: int, iss_num_end: int):
    m = api_auth()
    result = []
    for i in range(iss_num_start, iss_num_end + 1):
        result.append(m.issues_list({'series_name': series_name, 'series_year_began': series_year_began, 'number': i}))
    return HttpResponse('All good')


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

def api_auth():
    dotenv_path = os.path.expanduser('~/Documents/Personal_Projects/.env')
    load_dotenv(dotenv_path)
    username = os.getenv('METRON_USERNAME')
    password = os.getenv('METRON_PASSWORD')
    m = mokkari.api(username, password)
    return m

if __name__ == '__main__':
    m = api_auth()
    iss_id = []
    response = m.issues_list({'series_name': 'Black Widow', 'series_year_began': 2014})
    for item in response:
        iss_id.append(item.id)
    start_iss_num = 1
    end_iss_num = 5
    num_issues = end_iss_num - start_iss_num + 1
    first_iss = m.issues_list({'series_name': 'Black Widow', 'series_year_began': 2014, 'number': start_iss_num})
    start_idx = iss_id.index(first_iss.issues[0].id)
    for i in range(start_idx, start_idx + num_issues):
        print(m.issue(iss_id[i]).number)
                    