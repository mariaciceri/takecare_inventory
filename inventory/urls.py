from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.shortcuts import render

urlpatterns = [
    path('', include('ordering.urls'), name='ordering_urls'),
    path('home/', include('home.urls'), name='home_urls'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]


def custom_404(request, exception):
    return render(request, 'errors/error-404.html', status=404)


def custom_500(request):
    return render(request, 'errors/error-500.html', status=500)


handler404 = custom_404
handler500 = custom_500
