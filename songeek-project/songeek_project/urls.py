from django.urls import path
from songeek_project import views

app_name = 'songeek'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('add_album/', views.add_album, name='add_album'),
    path('album_list/', views.album_list, name='album_list'),
    path('album/<slug:album_name_slug>/', views.show_album, name='show_album'),
    path('add_song_to_playlist/', views.add_song_to_playlist, name='add_song_to_playlist'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('new_playlist/', views.new_playlist, name='new_playlist'),
    path('album/<slug:album_name_slug>/add_song_to_album/', views.add_song_to_album, name='add_song_to_album'),
]