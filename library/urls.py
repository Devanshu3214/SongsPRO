
from django.urls import path,include
from library import views
from django.contrib.auth import views as auth_views
from .views import register

urlpatterns = [
    path('', views.home, name='home'),
    path('recommendations/', views.song_recommendation, name='song_recommendation'),
    path('delete_song/', views.delete_song, name='delete_song'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_songs/', views.add_songs, name='add_songs'),
    path('add_rec_songs/', views.add_rec_songs, name='add_rec_songs'),
    path('song_list/', views.song_list, name='song_list'),
    path('export_to_excel/', views.export_to_excel, name='export_to_excel'),
]
