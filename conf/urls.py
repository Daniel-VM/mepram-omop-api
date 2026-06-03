from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="swagger-ui", permanent=False)),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url="/openapi/"),
        name="swagger-ui",
    ),
    path("v1/", include("core.api.v1.urls")),
]
