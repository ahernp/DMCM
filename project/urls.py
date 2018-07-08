from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/pages/home"), name="homepage"),
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.v1.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("pages/", include("mpages.urls")),
    path("core/", include("core.urls")),
    path("timers/", include("timers.urls")),
    path("tools/", include("tools.urls")),
]
