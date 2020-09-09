from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('betapp.urls')),
    path('admin/', admin.site.urls),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/favicon.ico')),
]
