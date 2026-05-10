from django.contrib import admin
from .models import SIEMAlertLog

@admin.register(SIEMAlertLog)
class SIEMAlertLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'agent_id', 'ip_address', 'threat_score', 'action_taken')
    list_filter = ('action_taken',)
    search_fields = ('agent_id', 'ip_address')
    readonly_fields = ('alert_id', 'timestamp', 'agent_id', 'ip_address', 'threat_score', 'action_taken')

    # Keamanan Zero-Trust: Log audit tidak boleh diubah/dihapus manual
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
