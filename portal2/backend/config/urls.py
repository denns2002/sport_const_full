from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


api = "api/"

urlpatterns = [
    path(api + "admin/", include("admincustom.urls")),  # Admin
    path(api + "users/", include("users.urls")),  # Users, reg, login etc.
    path(api + "profiles/", include("profiles.urls")),  # Users profiles
    path(api + "", include("clubs_groups.urls")),  # Groups and Clubs
    path(api + "events/", include("events.urls")),  # Events
    path(api + "statements/", include("statements.urls")),  # Statements
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_view = get_schema_view(
    openapi.Info(
        title="portal",
        default_version="v0.1",
        description="be sport",
        terms_of_service="nope",
        contact=openapi.Contact(email="denis.israfilov2002@mail.ru"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [  # SWAGGER
    path(
        api + "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        api + "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]