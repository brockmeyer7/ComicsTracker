from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<str:name>/<int:year>', views.book, name='book'),
    path('character/<str:name>', views.character, name = 'character')
]