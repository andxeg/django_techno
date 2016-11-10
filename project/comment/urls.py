from django.http import HttpResponseNotFound
from django.conf.urls import url
from comment import views


def return_http404(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')

urlpatterns = [
    url(r'^all$', views.comments_list, name='comments_list'),
    url(r'^user_(\d+)$', views.comments_by_user_id, name='comments_by_user_id'),
    url(r'^(\d+)$', views.comment_by_id, name='comment_by_id'),
    url(r'', return_http404, name='return_http404'),
]
