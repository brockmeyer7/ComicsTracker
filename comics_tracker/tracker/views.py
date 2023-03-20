from django.shortcuts import render
from django.http import HttpResponse
import json
from concurrent.futures import as_completed
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

        response = cv.get_series(name=series_name, offset=offset, params=['id', 'name', 'description', 'image'])
        results = json.loads(response)

        return render(request, 'series_results.html', results)
    
                    