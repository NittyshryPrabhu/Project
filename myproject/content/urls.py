from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('movies/', views.movies_view, name='movies'),
    path('webseries/', views.webseries_view, name='webseries'),
    path('shortfilm/', views.shortfilm_view, name='shortfilm'),
    path('social-content/', views.socialcontent_view, name='socialcontent'),
    path('watch/<slug:slug>/', views.watch_view, name='content_watch'),
]