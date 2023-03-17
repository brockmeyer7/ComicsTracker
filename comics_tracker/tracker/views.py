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
def search_series(request):
    if request.method =='GET':
        return render(request, 'search_series.html')
    
    if request.method == 'POST':
        series_name = request.POST['series_name']
        # limit = body['limit']
        if 'offset' in request.POST:
            offset = request.POST['offset']
        else:
            offset = 0

        response = cv.get_series(series_name, offset, 'id', 'name', 'description')
        series = json.loads(response)

        return HttpResponse(str(series))
    
                    