from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),
    url(r'^(?P<hash_value>[A-Za-z0-9]*)/$', views.page_redirect, name='page_redirect')
]