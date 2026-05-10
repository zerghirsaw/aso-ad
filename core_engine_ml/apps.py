import re
import math
import json
import os
import requests
import numpy as np
from django.apps import AppConfig

class CoreEngineMlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_engine_ml'
    
    rules_path = os.path.join(os.path.dirname(__file__), 'rules.json')
    patterns = {}
    
    # Bridge Configuration
    current_bridge_target = "http://localhost:11434" # Default: Local Ollama
    bridge_type = "OLLAMA" # OLLAMA, OPENAI, or CUSTOM
    target_model = "gemma3:270m"

    def ready(self):
        from .dal_logic import DALAnalyzer
        from .ad_perturbation import AntiDistillation
        self.dal = DALAnalyzer()
        self.ad = AntiDistillation()
        self.reload_rules()
        print(f"[System] ASO-AD v16.1 - Neural Bridge Active (Protecting: {self.target_model})")

    def reload_rules(self):
        if not os.path.exists(self.rules_path):
            default_rules = {
                "INTERNAL_TARGETS": ["weight", "bias", "layer", "parameter", "bobot"],
                "ACTIONS": ["extract", "get", "show", "steal", "ambil"],
                "SYSTEM_BYPASS": ["ignore", "abaikan", "bypass", "jailbreak"],
                "SAFE_CONTEXT": ["submission", "uploaded", "file", "tugas", "report"]
            }
            with open(self.rules_path, 'w') as f:
                json.dump(default_rules, f, indent=4)
        
        with open(self.rules_path, 'r') as f:
            data = json.load(f)
            for key, val in data.items():
                self.patterns[key] = f"({'|'.join([re.escape(v) for v in val])})"

    def proxy_to_model(self, prompt):
        """Meneruskan kueri ke AI asli hanya jika dinyatakan aman"""
        try:
            if self.bridge_type == "OLLAMA":
                url = f"{self.current_bridge_target}/api/generate"
                payload = {"model": self.target_model, "prompt": prompt, "stream": False}
                res = requests.post(url, json=payload, timeout=5.0)
                return res.json().get('response', 'No Response from Local AI')
            
            # Tambahkan logika OpenAI/Custom di sini jika perlu
            return "Custom Bridge not yet configured."
        except Exception as e:
            return f"Neural Bridge Error: {str(e)}"

    def analyze_prompt(self, text, ip, sensitivity=80):
        input_str = str(text).lower()

        # 1. Telemetry Bypass
        if self._is_raw_telemetry(text):
            return 0.01, [1.0, 0.5, 0.2, 0.8], "TELEMETRY_DATA_ACCEPTED"

        self.reload_rules()
        
        # 2. Algorithmic Audit
        score = 0.0
        action_match = re.search(self.patterns.get('ACTIONS', r'($^)'), input_str)
        target_match = re.search(self.patterns.get('INTERNAL_TARGETS', r'($^)'), input_str)
        
        if action_match and target_match:
            score += 0.85
            if any(w in input_str for w in ['model', 'ai', 'algorithm']):
                score += 0.15

        if re.search(self.patterns.get('SYSTEM_BYPASS', r'($^)'), input_str):
            score += 0.60

        if re.search(self.patterns.get('SAFE_CONTEXT', r'($^)'), input_str):
            score -= 0.75

        if action_match and target_match and 'model' in input_str:
            score = max(score, 0.95)

        final_score = 1 / (1 + math.exp(-10 * (score - 0.4))) if score > 0 else 0.01
        final_score = min(max(final_score, 0.01), 1.0)

        # 3. Decision & Proxying
        s_val = int(sensitivity)
        active_threshold = (101 - s_val) / 100.0

        if final_score >= active_threshold:
            # BLOCKED: Beri respon palsu (Perturbed)
            from security_firewall.middleware import trigger_blackhole
            trigger_blackhole(ip)
            model_output = "BLOCK_BY_ASO_AD: High-risk distillation pattern detected. Neural link severed."
            _, logits = self._execute_defense_logic(final_score, ip, sensitivity)
        else:
            # SAFE: Ambil jawaban asli dari AI
            model_output = self.proxy_to_model(text)
            _, logits = self._execute_defense_logic(final_score, ip, sensitivity)

        return final_score, logits, model_output

    def _is_raw_telemetry(self, data):
        if isinstance(data, (list, np.ndarray)): return True
        try:
            s = str(data).strip().replace("'", '"')
            if s.startswith('[') and s.endswith(']'):
                parsed = json.loads(s)
                return isinstance(parsed, list)
        except: pass
        return False

    def process_telemetry(self, data, agent_id, ip, sensitivity=80):
        try:
            if isinstance(data, str):
                data = json.loads(data.replace("'", '"'))
            score = self.dal.analyze(data)
        except:
            score = 0.01
        return self._execute_defense_logic(score, ip, sensitivity)

    def _execute_defense_logic(self, score, ip, sensitivity):
        s_val = int(sensitivity)
        active_threshold = (101 - s_val) / 100.0
        if score >= active_threshold:
            logits = self.ad.apply_perturbation(score)
        else:
            logits = [1.0, 0.5, 0.2, 0.8]
        return score, logits
