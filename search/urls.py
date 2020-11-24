from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favourites_save', views.favourites_save, name='favourites_save'),
    path('delete', views.delete, name='delete'),

]