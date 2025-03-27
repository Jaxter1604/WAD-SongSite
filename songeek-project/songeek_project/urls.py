from django.urls import path
from songeek_project import views

app_name = 'songeek'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_results, name='search_results'),
    path('album/<slug:album_slug>/add_review/', views.add_review, name='add_review'),
    path('add_album/', views.add_album, name='add_album'),
    path('album_list/', views.album_list, name='album_list'),
    path('album/<slug:album_name_slug>/', views.show_album, name='show_album'),
    path('song/<int:song_id>/', views.show_song, name='show_song'),
    path('song/<int:song_id>/song_add_review', views.song_add_review, name='song_add_review'),
    path('album/<slug:album_name_slug>/add_song_to_album/', views.add_song_to_album, name='add_song_to_album'),
    path('new_playlist/', views.new_playlist, name='new_playlist'),
    path('playlist/<slug:playlist_name_slug>', views.show_playlist, name='show_playlist'),
    path('playlist/<slug:playlist_name_slug>/add_song_to_playlist/', views.add_song_to_playlist, name='add_song_to_playlist'),
]