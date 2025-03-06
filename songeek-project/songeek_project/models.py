import os
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Album(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128,)
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

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    title = models.CharField(max_length=128)
    listens = models.IntegerField(default=0)
    lenght = models.DurationField(default=0)

    def __str__(self):
        return str(self.title)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username