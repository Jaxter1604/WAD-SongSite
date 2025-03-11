import os
import sys
import django
from datetime import timedelta

# Set Django environment variables
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'songeek.settings')
django.setup()

from songeek_project.models import Album, Song, UserProfile
from django.contrib.auth.models import User

def populate():
    """Populate the database"""

    # create Album
    albums = [
        {'name': 'Album A', 'artist': 'Artist 1', 'cover': 'album_covers/51RhfDwBMhL.jpg'},
        {'name': 'Album B', 'artist': 'Artist 2', 'cover': 'album_covers/386b817e1c43e3a8ac08bc131f27d92a.1000x1000x1.png'},
        {'name': 'Album C', 'artist': 'Artist 3', 'cover': 'album_covers/unnamed-2024-08-04T164909.586-scaled.jpg'},
    ]

    album_objects = []
    for album_data in albums:
        album_obj, created = Album.objects.get_or_create(
            name=album_data['name'],
            artist=album_data['artist'],
            defaults={'cover': album_data['cover']}
        )
        album_objects.append(album_obj)

    # create Song
    songs = [
        {'title': 'Song A1', 'album': album_objects[0], 'length': 240},
        {'title': 'Song A2', 'album': album_objects[0], 'length': 180},
        {'title': 'Song B1', 'album': album_objects[1], 'length': 300},
        {'title': 'Song B2', 'album': album_objects[1], 'length': 210},
        {'title': 'Song C1', 'album': album_objects[2], 'length': 200},
        {'title': 'Song C2', 'album': album_objects[2], 'length': 250},
    ]

    for song_data in songs:
        Song.objects.get_or_create(
            title=song_data['title'],
            album=song_data['album'],
            defaults={'length': timedelta(seconds=song_data['length'])}  
        )

    # create users
    users = [
        {'username': 'user1', 'email': 'user1@example.com'},
        {'username': 'user2', 'email': 'user2@example.com'},
    ]

    for user_data in users:
        user_obj, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={'email': user_data['email']}
        )
        UserProfile.objects.get_or_create(user=user_obj)

    print("Database filling is completed!")

if __name__ == '__main__':
    populate()
