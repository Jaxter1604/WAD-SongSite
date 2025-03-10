from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from songeek_project import views
from django.contrib import admin
from django.urls import path

app_name = 'songeek'

urlpatterns = [
    path('', views.index, name='index'),
    path('songeek/', include('songeek_project.urls')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
