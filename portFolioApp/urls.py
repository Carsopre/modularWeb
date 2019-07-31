from django.urls import include, path
from . import views

app_name = 'portFolioApp'
urlpatterns = [
        path(
                'portfolio/<portfolio_slug>/',
                views.portfolioView,
                name='portfolioView'),
        # url(r'^404', views.not_found, {'exception': Exception()}),
]
