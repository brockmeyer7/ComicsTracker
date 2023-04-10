from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.views.decorators.http import require_http_methods
from tracker import comicvine_wrapper, models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

cv = comicvine_wrapper.ComicVine()

@login_required
def index(request):
    return render(request, 'base.html')


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.method=='GET':
        return render(request, 'login.html')
    
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')

@require_http_methods(['GET', 'POST'])
def sign_up(request):
    if request.method=='GET':
        return render(request, 'sign_up.html')
    
    if request.method=='POST':
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email= request.POST['email'])
        user.save()
        return redirect('index')

@login_required
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

@login_required
@require_http_methods(["GET"]) 
def series_issues(request, id):
    response = cv.get_issues(volume=id)
    results = json.loads(response)
    return render(request, 'series_issues.html', results)

