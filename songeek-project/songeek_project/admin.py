from django.contrib import admin
from songeek_project.models import Album, Song, UserProfile

# Register your models here.

class SongAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'album',
        'length',
    )

class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(UserProfile)