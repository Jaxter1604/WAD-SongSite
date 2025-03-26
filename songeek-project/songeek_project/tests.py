import json
import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from songeek_project.models import Album, Song, Playlist, Review
from datetime import timedelta


# Create your tests here.


class SongeekTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.album = Album.objects.create(name='Test Album', artist='Test Artist', slug='test-album')
        self.song = Song.objects.create(title='Test Song', album=self.album, length=timedelta(minutes=3))
        self.client.login(username='testuser', password='testpass')

    def test_album_model(self):
        self.assertEqual(self.album.name, 'Test Album')
        self.assertEqual(self.album.artist, 'Test Artist')
        self.assertEqual(str(self.album), 'Test Album')

    def test_album_list_view(self):
        response = self.client.get(reverse('songeek:album_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.album.artist)

    def test_show_album_view(self):
        response = self.client.get(reverse('songeek:show_album', kwargs={'album_name_slug': self.album.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Song')

    def test_add_album_view(self):
        response = self.client.get(reverse('songeek:add_album'))
        self.assertEqual(response.status_code, 200)

        with open('media/album_covers/default.jpeg', 'rb') as img:
            response = self.client.post(reverse('songeek:add_album'), {
                'name': 'New Album',
                'artist': 'New Artist',
                'cover': img,
            })
        self.assertEqual(response.status_code, 302)  # Redirect after success

        self.assertTrue(Album.objects.filter(name='New Album').exists())

    def test_user_registration(self):
        self.client.logout()
        response = self.client.post(reverse('songeek:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass',
        })
        self.assertNotEqual(response.status_code, 500)  # No crash

    def test_user_login(self):
        self.client.logout()
        response = self.client.post(reverse('songeek:login'), {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)  # redirect on success

    def test_ajax_add_review_view(self):
        url = reverse('songeek:add_review', kwargs={'album_slug': self.album.slug})
        data = {
            "rating": 5,
            "comment": "Amazing Album!"
        }

        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['rating'], 5)
        self.assertEqual(json_response['comment'], "Amazing Album!")
        self.assertEqual(json_response['user'], self.user.username)

        # Confirm that the comment is written into the database
        self.assertTrue(Review.objects.filter(album=self.album, user=self.user, comment="Amazing Album!").exists())
    
    def tearDown(self):
        folder = os.path.join(settings.MEDIA_ROOT, 'album_covers')
        for filename in os.listdir(folder):
            if filename.startswith('default_') and filename.endswith('.jpeg'):
                os.remove(os.path.join(folder, filename))
