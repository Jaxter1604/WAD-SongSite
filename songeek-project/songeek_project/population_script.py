import os
import sys
import django
from datetime import timedelta

# Set Django environment variables
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'songeek.settings')
django.setup()

from songeek_project.models import Album, Song, UserProfile, Review
from django.contrib.auth.models import User

def populate():
    """Populate the database"""
    print("Starting database population...")

    # create Album
    albums = [
        {'name': 'Album A', 'artist': 'Artist 1', 'cover': 'album_covers/51RhfDwBMhL.jpg', 'likes': 100},
        {'name': 'Album B', 'artist': 'Artist 2', 'cover': 'album_covers/386b817e1c43e3a8ac08bc131f27d92a.1000x1000x1.png', 'likes': 200},
        {'name': 'Album C', 'artist': 'Artist 3', 'cover': 'album_covers/unnamed-2024-08-04T164909.586-scaled.jpg', 'likes': 300},
    ]

    album_objects = []
    for album_data in albums:
        album_obj, created = Album.objects.get_or_create(
            name=album_data['name'],
            artist=album_data['artist'],
            defaults={'cover': album_data['cover'], 'likes': album_data['likes']}
        )
        album_objects.append(album_obj)

    print(f"Added {len(album_objects)} albums.")

    # create Song
    songs = [
        {'title': 'Song A1', 'album': album_objects[0], 'length': '04:00'},
        {'title': 'Song A2', 'album': album_objects[0], 'length': '03:00'},
        {'title': 'Song B1', 'album': album_objects[1], 'length': '05:00'},
        {'title': 'Song B2', 'album': album_objects[1], 'length': '03:30'},
        {'title': 'Song C1', 'album': album_objects[2], 'length': '03:20'},
        {'title': 'Song C2', 'album': album_objects[2], 'length': '04:10'},
    ]

    for song_data in songs:
        Song.objects.get_or_create(
            title=song_data['title'],
            album=song_data['album'],
            defaults={'length': timedelta(minutes=int(song_data['length'].split(':')[0]), 
                                          seconds=int(song_data['length'].split(':')[1]))}  
        )

    print(f"Added {len(songs)} songs.")

    # create users
    users = [
        {'username': 'user1', 'email': 'user1@example.com'},
        {'username': 'user2', 'email': 'user2@example.com'},
    ]

    user_objects = []
    for user_data in users:
        user_obj, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={'email': user_data['email']}
        )
        user_objects.append(user_obj)
        UserProfile.objects.get_or_create(user=user_obj)

    print(f"Added {len(user_objects)} users.")

    # Add Review 
    reviews_data = [
        {'user': User.objects.first(), 'album': Album.objects.first(), 'rating': 5, 'comment': 'Awesome!'},
        {'user': User.objects.last(), 'album': Album.objects.last(), 'rating': 4, 'comment': 'Great album!'}
    ]

    for review_data in reviews_data:
        user = review_data['user']
        album = review_data['album']

        if user and album:
            review, created = Review.objects.update_or_create(
                user=user,
                album=album,
                defaults={'rating': review_data['rating'], 'comment': review_data['comment']}
            )

            if created:
                print(f"Added review: {review}")
            else:
                print(f"Updated existing review: {review}")
        else:
            print("Skipping review, missing user or album.")

    print("Database filling is completed!")

if __name__ == '__main__':
    populate()
