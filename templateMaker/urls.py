from django.urls import path, include
from . import views

urlpatterns = [
        path('', views.get_name, name='name'),
        # path(r'^404', views.not_found, {'exception': Exception()}),
]
