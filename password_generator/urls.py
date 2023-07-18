from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from generator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('password', views.password, name='password'),
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path("contact", views.contact, name="contact"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
