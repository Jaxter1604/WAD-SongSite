from django import template
from songeek_project.models import Album

register = template.Library()

@register.inclusion_tag('songeek/album_list.html')
def get_album_list(current_album=None):
    return {'albums': Album.objects.all(),
            'current_album': current_album}

# @register.inclusion_tag('songeek/profile.html')
# def get_playlists(current_album=None):
#     return {'playlists': Playlist.objects.all(),
#             'current_playlist': current_playlist}