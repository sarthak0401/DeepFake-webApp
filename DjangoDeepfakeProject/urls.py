from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('upload/', views.upload_image, name='upload_image'),
    path('show_result/', views.show_result, name='show_result'),

    path('__reload__/', include('django_browser_reload.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)