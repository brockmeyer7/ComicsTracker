from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search_series', views.search_series, name='search_series'),
    path('series_issues/<str:id>', views.series_issues, name='series_issues'),
    path('login', views.login_view, name='login'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('logout', views.logout_view, name='logout')
]