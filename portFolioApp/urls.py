from django.urls import include, path
from . import views

app_name = 'portFolioApp'
urlpatterns = [
        path(
                'portfolio/<page_slug>/',
                views.render_page,
                name='render_page'),
        # url(r'^404', views.not_found, {'exception': Exception()}),
]
