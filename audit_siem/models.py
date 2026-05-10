from django.db import models
import uuid

class SIEMAlertLog(models.Model):
    # Menggunakan UUID untuk keamanan, mencegah penyerang menebak ID urutan log
    alert_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_id = models.CharField(max_length=255, db_index=True)
    ip_address = models.GenericIPAddressField()
    threat_score = models.FloatField()
    action_taken = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'siem_alert_logs'
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.action_taken}] Score: {self.threat_score} | Agent: {self.agent_id}"
