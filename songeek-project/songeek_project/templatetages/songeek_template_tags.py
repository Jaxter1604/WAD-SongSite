from django import template
from songeek_project.models import Album

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_album_list(current_album=None):
    return {'categories': Album.objects.all(),
            'current_category': current_album}