from django.contrib import admin
from django.urls import path

admin.site.site_header = "Aikido Administration"
admin.site.index_title = "All tables:"

urlpatterns = [
    path("", admin.site.urls),
]
