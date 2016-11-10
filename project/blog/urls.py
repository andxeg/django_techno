from django.http import HttpResponseNotFound
from django.conf.urls import url
from blog import views


def return_http404(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')

urlpatterns = [
    url(r'^post/all$', views.posts_list, name='post_list'),
    url(r'^post/(\d+)$', views.post_by_id, name='post_by_id'),
    url(r'^post/user_(\d+)$', views.posts_by_user_id, name='posts_by_user_id'),
    url(r'^category/all$', views.categories_list, name='categories_list'),
    url(r'^category/(\d+)$', views.category_by_id, name='category_by_id'),
    url(r'', return_http404, name='return_http404'),
]
