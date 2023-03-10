from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<str:series_name>/<int:series_year_began>/<int:issue_number_after>/<int:issue_number_before>', views.book, name='book'),
    path('character/<str:name>', views.character, name = 'character')
]