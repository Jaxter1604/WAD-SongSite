from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

# model works with example in admin database and index.html
# (index.html as of 7/3/25 8:50)
class Album(models.Model):
    name = models.CharField(max_length=128)
    artist = models.CharField(max_length=128)
    likes = models.IntegerField(default=0)
    cover = models.ImageField(upload_to='album_covers', default="album_covers/default.jpeg")
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Album, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Albums'
        app_label = 'songeek_project'

    def __str__(self):
        return str(self.name)

# model untested but simple enough to work or fix
# song cannot exist without album
# i.e. have to go into the album page before adding it
# avoids needing to use complex form cleaning like with
# adding songs to playlists
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
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
    slug = models.SlugField(unique=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Playlist, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Playlists'
        app_label = 'songeek_project'
    
    def __str__(self):
        return str(self.name)

#basic user model from rango
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/profile_photo.jpg')

    def __str__(self):
        return self.user.username

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices = [(i, i) for i in range(1,6)])
    comment = models.TextField(blank=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'album'), ('user', 'song'))
        app_label = 'songeek_project'
    