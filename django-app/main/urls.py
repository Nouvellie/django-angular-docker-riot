from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("main-admin/", admin.site.urls),

    path('', include('apps.core.urls'),),
]
