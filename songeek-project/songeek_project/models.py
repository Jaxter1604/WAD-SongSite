import os
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

# model works with example in admin database and index.html
# (index.html as of 7/3/25 8:50)
class Album(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    artist = models.CharField(max_length=128)
    likes = models.IntegerField(default=0)
    cover = models.ImageField(upload_to='album_covers', blank = True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Album, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Albums'

    def __str__(self):
        return str(self.name)

# model untested but simple enough to work or fix
# song cannot exist without album
# i.e. have to go into the album page before adding it
# avoids needing to use complex form cleaning like with
# adding songs to playlists
class Song(models.Model):
    id = models.AutoField(primary_key=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    title = models.CharField(max_length=128)
    listens = models.IntegerField(default=0)
    length = models.DurationField(default=0)

    def __str__(self):
        return str(self.title)

# model untested and needs from page to do so
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    cover = models.ImageField(upload_to='playlist_covers', blank = True)
    songs = models.ManyToManyField(Song, related_name='playlists', blank = True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Playlist, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Playlists'
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"

#basic user model from rango
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

# might not need Primary key for id here
# must be owned by a user and belong to an album and its page
# review will be restricted between 1-5 or 1-10, 0 NA
# automatic timestamp
class AlbumReview(models.Model):
    id = models.AutoField(primary_key=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default = 1)
    review = models.TextField(max_length=1000)
    timeStamp = models.DateTimeField(auto_now_add=True)

    # spacing may not work for plural
    class Meta:
        verbose_name_plural = 'Album Reviews'

    # not sure if this is needed or correct
    def __str__(self):
        return str(self.id)

class SongReview(models.Model):
    id = models.AutoField(primary_key=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default = 1)
    review = models.TextField(max_length=1000)
    timeStamp = models.DateTimeField(auto_now_add=True)

    # spacing may not work for plural
    class Meta:
        verbose_name_plural = 'Song Reviews'

    # not sure if this is needed or correct
    def __str__(self):
        return str(self.id)
    