from django.contrib import admin
from django.urls import path
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
]

websocket_urlpatterns = [

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
