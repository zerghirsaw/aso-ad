import os
import json
import redis
import math
from django.shortcuts import render
from django.apps import apps
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import TelemetrySerializer
from security_firewall.middleware import check_threat_throttle
from audit_siem.models import SIEMAlertLog

class ASOEndpointView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @check_threat_throttle
    def post(self, request):
        # Ambil data mentah
        raw_payload = request.data.get('telemetry')
        agent_id = request.data.get('agent_id', 'TAC_NODE_01')
        
        # --- AMBIL PARAMETER SENSITIVITY (Dukungan Angka 1-100) ---
        sensitivity = request.data.get('sensitivity', 80)
        
        ip = request.META.get('REMOTE_ADDR')
        engine = apps.get_app_config('core_engine_ml')

        try:
            # LOGIKA DETEKSI GANDA: TEXT vs NUMERIC
            if isinstance(raw_payload, str):
                # JALUR SEMANTIK (Neural Bridge Mode)
                # FIX: Tangkap 3 Nilai (score, logits, model_output)
                score, logits, model_output = engine.analyze_prompt(raw_payload, ip, sensitivity)
                status_msg = "NEURAL_PROXY_COMPLETE"
            else:
                # JALUR TELEMETRI (Numeric Array)
                serializer = TelemetrySerializer(data=request.data)
                if not serializer.is_valid():
                    return Response({"error": "Malformed Numeric Data"}, status=status.HTTP_400_BAD_REQUEST)
                
                score, logits = engine.process_telemetry(raw_payload, agent_id, ip, sensitivity)
                status_msg = "TELEMETRY_PROCESSED"
                model_output = "SENSOR_DATA_BYPASSED" # Dummy text agar frontend aman

            # Anti-Overload Check (Nan/Inf protection)
            if math.isnan(score) or math.isinf(score):
                score = 1.0

            # Logging ke SIEM
            if score > 0.8:
                action = "MODEL_DISTILLATION_BLOCKED" if isinstance(raw_payload, str) else "AD_SHIELD_ACTIVATED"
                SIEMAlertLog.objects.create(
                    agent_id=agent_id,
                    ip_address=ip,
                    threat_score=round(score, 4),
                    action_taken=f"{action} [SENSITIVITY_VAL:{sensitivity}]"
                )

            return Response({
                "status": status_msg, 
                "score": round(score, 4), 
                "logits": logits,
                "model_output": model_output, # <--- TAMBAHAN KRUSIAL UNTUK DASHBOARD V16.1
                "input_type": "neural_text" if isinstance(raw_payload, str) else "telemetry_data",
                "defense_mode": f"PROXY_LEVEL_{sensitivity}"
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "status": "CRITICAL_OVERLOAD", 
                "score": 1.0, 
                "logits": [0.0, 0.0, 0.0, 0.0],
                "model_output": f"BRIDGE_ERROR: {str(e)}",
                "error": str(e)
            }, status=status.HTTP_200_OK)

class ModelConnectView(APIView):
    """Menghubungkan Universal Neural Bridge ke Endpoint Baru"""
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        url = request.data.get('model_url')
        if not url:
            return Response({"error": "URL Required"}, status=status.HTTP_400_BAD_REQUEST)
        
        engine = apps.get_app_config('core_engine_ml')
        
        # Modifikasi Target Bridge secara Dinamis
        engine.current_bridge_target = url
        if "openai.com" in url:
            engine.bridge_type = "OPENAI"
        else:
            engine.bridge_type = "OLLAMA"
            
        return Response({
            "status": "BRIDGE_ESTABLISHED", 
            "target": url,
            "type": engine.bridge_type
        })

class ResetVaultView(APIView):
    """Membersihkan Redis Blackhole secara ABSOLUT"""
    permission_classes = [AllowAny] 
    authentication_classes = []
    
    def _flush_redis_nuke(self):
        cache.clear()
        try:
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.flushall()
        except Exception as e:
            print(f"[ERROR] Redis Nuke Failed: {e}")
            
    def get(self, request): 
        self._flush_redis_nuke()
        return Response({"status": "VAULT_CLEARED_ABSOLUTE (GET)"})
        
    def post(self, request):
        self._flush_redis_nuke()
        return Response({"status": "VAULT_CLEARED_ABSOLUTE (POST)"})

class DashboardView(APIView):
    """Menampilkan Tactical Console Dashboard"""
    permission_classes = [AllowAny]
    def get(self, request):
        return render(request, 'api_gateway/dashboard.html')


# --- TAMBAHAN BARU: RULES MANAGEMENT API ---
class RulesManagementView(APIView):
    """API untuk Manajemen Aturan (Add, Remove, View) di rules.json secara dinamis"""
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_engine(self):
        return apps.get_app_config('core_engine_ml')

    def get(self, request):
        """Membaca isi rules.json untuk ditampilkan di Dashboard"""
        engine = self.get_engine()
        if os.path.exists(engine.rules_path):
            with open(engine.rules_path, 'r') as f:
                rules = json.load(f)
            return Response(rules)
        return Response({"error": "Rules file not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Menambah atau Menghapus kata dari rules.json"""
        action = request.data.get('action') # Isinya: 'add' atau 'remove'
        category = request.data.get('category')
        word = request.data.get('word')

        if not all([action, category, word]):
            return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        engine = self.get_engine()
        try:
            with open(engine.rules_path, 'r') as f:
                rules = json.load(f)

            if category not in rules:
                rules[category] = []

            word = word.lower().strip()

            if action == 'add':
                if word not in rules[category]:
                    rules[category].append(word)
            elif action == 'remove':
                if word in rules[category]:
                    rules[category].remove(word)

            # Simpan kembali ke file json
            with open(engine.rules_path, 'w') as f:
                json.dump(rules, f, indent=4)

            # RELOAD aturan di Engine agar langsung berefek tanpa restart server!
            engine.reload_rules() 
            return Response({"status": "SUCCESS", "rules": rules})
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
