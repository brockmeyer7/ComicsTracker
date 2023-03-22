from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search_series', views.search_series, name='search_series'),
    path('series_issues/<str:id>', views.series_issues, name='series_issues')
]