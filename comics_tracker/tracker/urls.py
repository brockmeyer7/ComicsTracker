from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<str:title>/<int:start_year>/<int:iss_start_num>/<int:iss_end_num>', views.book, name='book'),
    path('character/<str:name>', views.character, name = 'character')
]