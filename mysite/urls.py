from django.conf.urls import include, url
from django.conf.urls import handler404, handler500
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('modularweb.urls', namespace='modularweb')),
]

handler404 = 'modularweb.views.not_found'