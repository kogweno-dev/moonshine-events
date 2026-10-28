from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Moonshine Events admin"
admin.site.site_title = "Moonshine Events"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
