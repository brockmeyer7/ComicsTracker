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
from mokkari_api import MokkariSession

m = MokkariSession()

def index(request):
    return HttpResponse("Hello World!")

@require_http_methods(['GET', 'POST'])
def book(request, series_name: str, series_year_began: int, iss_num_start: int, iss_num_end: int):
    if request.method == 'POST':
        m.iss_list_lookup(series_name=series_name, series_year_began=series_year_began)


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
    m = MokkariSession()
    series_name = 'Thor'
    iss_id = []
    series = api_auth().series_list()
    for item in series:
        print(item.series)
        # if item.name[0:len(series_name)] == series_name:
        #     series_id = item.id
        #     break
    # response = m.iss_list_lookup(series_name, 2018)
    # for item in response:
    #     if item.issue_name[0:len(series_name)] == series_name:
    #         iss_id.append(item.id)
    # start_iss_num = 1
    # end_iss_num = 4
    # num_issues = end_iss_num - start_iss_num + 1
    # first_iss = api_auth().issues_list({'series_id': series_id, 'series_year_began': 2018, 'number': start_iss_num})
    # start_idx = iss_id.index(first_iss.issues[0].id)
    # for i in range(start_idx, start_idx + num_issues):
    #     issue = m.single_issue(iss_id[i])
    #     print(issue.id, issue.series.name, issue.number)
                    