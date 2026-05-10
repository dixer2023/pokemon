from django.urls import path
from . import views

app_name = 'pokedex'

urlpatterns = [
    path('', views.index, name='index'),
    path('pokemon/<int:pk>/', views.pokemon_detail, name='detail'),
    path('download-library/', views.download_library, name='download_library'),
]
