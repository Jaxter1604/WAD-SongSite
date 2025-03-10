import sys
import os
import django

# Set Django environment variables
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'songeek.settings')
django.setup()

from songeek_project.models import Album, Song, UserProfile
from datetime import timedelta
from django.contrib.auth.models import User

def populate():
    """Populate the database with data"""

    # Define some initial albums
    albums = [
        {'name': 'Album A', 'artist': 'Artist 1', 'likes': 50},
        {'name': 'Album B', 'artist': 'Artist 2', 'likes': 30},
        {'name': 'Album C', 'artist': 'Artist 3', 'likes': 70},
    ]

    album_objects = []
    for album in albums:
        obj, created = Album.objects.get_or_create(
            name=album['name'],
            artist=album['artist'],
            defaults={'likes': album['likes']}
        )
        album_objects.append(obj)

    # Define some songs (2 songs per album)
    songs = [
        {'title': 'Song A1', 'album': album_objects[0], 'listens': 100, 'length': timedelta(seconds=200)},
        {'title': 'Song A2', 'album': album_objects[0], 'listens': 150, 'length': timedelta(seconds=250)},
        {'title': 'Song B1', 'album': album_objects[1], 'listens': 80, 'length': timedelta(seconds=180)},
        {'title': 'Song B2', 'album': album_objects[1], 'listens': 90, 'length': timedelta(seconds=210)},
        {'title': 'Song C1', 'album': album_objects[2], 'listens': 200, 'length': timedelta(seconds=240)},
        {'title': 'Song C2', 'album': album_objects[2], 'listens': 250, 'length': timedelta(seconds=300)},
    ]

    for song in songs:
        Song.objects.get_or_create(
            title=song['title'],
            album=song['album'],
            defaults={
                'listens': song['listens'],
                'length': song['length']  
            }
        )

    # Create some users (for example)
    users = [
        {'username': 'user1', 'email': 'user1@example.com'},
        {'username': 'user2', 'email': 'user2@example.com'},
    ]

    
    for user_data in users:
        user_obj, created = User.objects.get_or_create(username=user_data['username'], defaults={'email': user_data['email']})

        UserProfile.objects.get_or_create(user=user_obj)

    print("The database has been filled up!")

if __name__ == '__main__':
    populate()
