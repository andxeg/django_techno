from django.http import HttpResponseNotFound
from django.conf.urls import url
from polls import views


def return_http404(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')

urlpatterns = [
    url(r'^all$', views.polls_list, name='post_list'),
    url(r'^(\d+)$', views.polls_by_user_id, name='polls_by_user_id'),
    url(r'^choice/(\d+)$', views.get_choice_by_id, name='get_choice_by_id'),
    url(r'^time$', views.current_datetime, name='current_datetime'),
    url(r'', return_http404, name='return_http404'),
]
