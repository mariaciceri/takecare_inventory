from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('ordering.urls'), name='ordering_urls'),
    path('home/', include('home.urls'), name='home_urls'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]
