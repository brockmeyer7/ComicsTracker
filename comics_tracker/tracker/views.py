from django.shortcuts import render
from django.http import HttpResponse
import hashlib
import calendar, time
import requests, json
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.views.decorators.http import require_http_methods
from tracker import comicvine_wrapper, models

cv = comicvine_wrapper.ComicVine()

def index(request):
    return HttpResponse("Hello World!")

@require_http_methods(['GET', 'POST'])
def book(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        series_name = body['name']
        start_year = body['start_year']

        response = cv.get_volume(series_name, start_year, 'id', 'name', 'start_year', 'first_issue', 'last_issue')
        data = json.loads(response)


        return HttpResponse(str(data))
    
                    