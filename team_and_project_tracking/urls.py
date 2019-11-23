"""team_and_project_tracking URL Configuration"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView


urlpatterns = [
    path('team_project_tracking/', include('team_project_tracking.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    # path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='/team_project_tracking/', permanent=False)),
    re_path(r'^u/', include('unfriendly.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)