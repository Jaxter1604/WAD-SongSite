from django import template
from songeek_project.models import Album

register = template.Library()

@register.inclusion_tag('songeek/album_list.html')
def get_album_list(current_album=None):
    return {'categories': Album.objects.all(),
            'current_category': current_album}