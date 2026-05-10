from rest_framework import serializers

class TelemetrySerializer(serializers.Serializer):
    agent_id = serializers.CharField(max_length=255)
    telemetry = serializers.ListField(
        child=serializers.FloatField(min_value=0.0, max_value=100.0),
        min_length=3,
        max_length=100
    )

    def validate_telemetry(self, value):
        if sum(value) == 0:
            raise serializers.ValidationError("Entropy detection: payload rejected.")
        return value
