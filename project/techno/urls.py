"""techno URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views
from django.shortcuts import render
from django.conf.urls import include, url
from django.http import HttpResponse
from django.http import HttpResponseNotFound


def return_http404(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')


def return_main_page(request):
    return render(request, './custom_user/main_page.html', {"username": request.user})


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login, {
        'template_name': './custom_user/login.html'
    }),
    url(r'^main_page/', return_main_page, name="return_main_page"),
    url(r'^poll/', include('polls.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^comment/', include('comment.urls')),
    # url(r'^users/', include('blog.urls')),
    url(r'', return_http404, name="return_http404"),
]

# i must do main page
# when user login in main page load
