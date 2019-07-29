from django.urls import include, path
from . import views

app_name = 'mainApp'
urlpatterns = [
        path(
                'index',
                views.index,
                name='home'),
        path(
                'home',
                views.index,
                name='home'),
        path(
                '',
                views.index,
                name='home'),
        path(
                '<page_type>/<page_slug>/',
                views.render_page,
                name='render_page'),
        # url(r'^404', views.not_found, {'exception': Exception()}),
]
