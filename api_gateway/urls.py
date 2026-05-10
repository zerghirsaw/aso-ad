from django.urls import path
from .views import ASOEndpointView, ModelConnectView, ResetVaultView, DashboardView, RulesManagementView

urlpatterns = [
    path('telemetry/', ASOEndpointView.as_view(), name='aso_telemetry'),
    path('connect-model/', ModelConnectView.as_view(), name='connect_model'),
    path('reset-vault/', ResetVaultView.as_view(), name='reset_vault'),
    
    # Cukup tulis 'rules/' saja, karena 'api/' nya sudah di-handle di root
    path('rules/', RulesManagementView.as_view(), name='rules_management'), 
]
