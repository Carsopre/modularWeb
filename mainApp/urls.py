from django.conf.urls import include, url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='home'),
        url('index', views.index, name='home'),
        url('home', views.index, name='home'),
        url(r'^section/(?P<pageSlug>[\w-]+)/$', views.render_page),
#        url(r'^404', views.not_found, {'exception': Exception()}),
]
