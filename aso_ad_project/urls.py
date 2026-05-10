from django.contrib import admin
from django.urls import path, include
from api_gateway.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_gateway.urls')),
    path('', DashboardView.as_view(), name='dashboard'), # Dashboard Utama
]
