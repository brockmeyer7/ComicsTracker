from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.http import require_http_methods
from tracker import comicvine_wrapper, models

cv = comicvine_wrapper.ComicVine()

def index(request):
    return render(request, 'base.html')

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method=='GET':
        return render(request, 'login.html')


@require_http_methods(['GET', 'POST'])
def search_series(request):
    if request.method =='GET':
        return render(request, 'search_series.html')
    
    if request.method == 'POST':
        series_name = request.POST['series_name']
        if 'offset' in request.POST:
            offset = request.POST['offset']
        else:
            offset = 0

        print(request.POST)
        response = cv.get_series(name=series_name, offset=offset, params=['id', 'name', 'image', 'start_year', 'publisher', 'first_issue', 'last_issue'])
        results = json.loads(response)['results']
        
        if request.POST['start_year'] != '':
            results = cv.filter_start_year(request.POST['start_year'], results)
        elif request.POST['publisher'] != '':
            results = cv.filter_publisher(request.POST['publisher'], results)
        else:
            results = results

        results_dict = {'results': results, 'offset': offset, 'series_name': series_name}

        return render(request, 'series_results.html', results_dict)

@require_http_methods(["GET"]) 
def series_issues(request, id):
    response = cv.get_issues(volume=id)
    results = json.loads(response)
    return render(request, 'series_issues.html', results)

