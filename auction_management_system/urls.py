from django.contrib import admin
from django.urls import path, include

from accounts import views
from django.conf.urls.static import static
from auction_management_system import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='home'),
    path('accounts/', include('accounts.urls')),
    path('auctions/', include('auctions.urls')),
    path('bids/', include('bids.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)