from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="swagger-ui1", permanent=False)),
    path("openapi/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url="/openapi/"),
        name="swagger-ui1",
    ),
    path("v1/", include("core.api.v1.urls")),
]
