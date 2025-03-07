from django.urls import path
from songeek_project import views

app_name = 'songeek'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('add_album/', views.add_album, name='add_album'),
    path('album_list/', views.album_list, name='album_list')
]