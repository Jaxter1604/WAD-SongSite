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
        is_new = self.pk is None  # Check if this is a new object

        super(Album, self).save(*args, **kwargs)  # Save first to generate an ID

        # Assign a unique slug based on the ID
        if is_new:
            self.slug = slugify(self.id)
            super(Album, self).save(update_fields=['slug'])

        # Rename the cover image file if uploaded
        if self.cover and hasattr(self.cover, 'path'):  # Ensure the file exists
            ext = os.path.splitext(self.cover.name)[1]  # Get file extension
            new_filename = f"{self.id}{ext}"  # Rename file to match ID
            new_path = os.path.join(settings.MEDIA_ROOT, 'album_covers', new_filename)
            old_path = self.cover.path  # Get current file path

            # Rename the file on disk if it exists and isn't already renamed
            if os.path.exists(old_path) and old_path != new_path:
                os.rename(old_path, new_path)  # Rename file in filesystem

            # Update the file path in the database
            self.cover.name = f"album_covers/{new_filename}"
            super(Album, self).save(update_fields=['cover'])

    class Meta:
        verbose_name_plural = 'Albums'

    def __str__(self):
        return str(self.name)

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    listens = models.IntegerField(default=0)
    length = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username