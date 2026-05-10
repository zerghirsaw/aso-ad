<img width="1912" height="1052" alt="pictureproduct" src="https://github.com/user-attachments/assets/7c873715-516a-4c33-8fac-d08eef056267" />
# ASO-AD: Active Shielding Overlay - Anti-Distillation

![Status](https://img.shields.io/badge/Status-Ironclad_Proxy_Active-00ff00?style=for-the-badge)
![Engine](https://img.shields.io/badge/Engine-Algo_V16.1-yellow?style=for-the-badge)
![Platform](https://img.shields.io/badge/Infrastructure-AI_Security-cyan?style=for-the-badge)

**ASO-AD** adalah *universal neural proxy* dan *security middleware* deterministik yang dirancang khusus untuk melindungi model AI dari serangan distilasi (*distillation attacks*), pencurian kekayaan intelektual (IP), dan *adversarial reverse-engineering* dengan *zero-latency overhead*.

## 🛡️ Masalah: Krisis Pencurian IP AI
Kompetitor dapat dengan mudah "memanen" logika dan bobot model AI Anda yang mahal melalui teknik *strategic querying* (Student-Teacher Distillation). Tanpa perlindungan, investasi R&D Anda dapat direplikasi hanya dalam hitungan menit.

## 🚀 Solusi: Active Shielding Overlay
ASO-AD berdiri di antara pengguna dan model AI Anda sebagai lapisan pelindung aktif yang mengaudit setiap request secara deterministik.

### Fitur Utama:
- **Zero-Latency Audit:** Menggunakan *Deterministic Scoring Accumulation* (Sub-5ms) alih-alih menggunakan AI auditor yang lambat.
- **AD-Shield (Logit Poisoning):** Tidak hanya memblokir, sistem ini memberikan *high-entropy noise* untuk merusak data latihan penyerang.
- **Universal Neural Bridge:** Terhubung secara mulus dengan **Ollama (Local)**, **OpenAI (Cloud)**, atau **Custom API Endpoints**.
- **Tactical CLI & Dashboard:** Manajemen aturan (*rules*) dinamis yang dapat di-*update* secara *real-time* tanpa mematikan layanan (Hot-Reload).
- **Ironclad SIEM:** Logging audit semantik untuk kebutuhan kepatuhan regulasi dan deteksi ancaman.

## 🏗️ Arsitektur Sistem
ASO-AD bekerja sebagai *Middleware Proxy* tingkat kernel:
1. **Intercept:** Menangkap prompt pengguna sebelum mencapai model target.
2. **Audit:** Menganalisis intent menggunakan algoritma akumulasi skor berbasis keyword dan konteks.
3. **Decide:** Jika aman, request diteruskan. Jika terdeteksi serangan distilasi, sistem mengaktifkan perisai.
4. **Poison:** (Opsional) Mengirimkan respon yang telah dimanipulasi untuk merusak model "student" penyerang.

## 🛠️ Tech Stack
- **Backend:** Python (Django Enterprise Architecture)
- **Frontend:** Tailwind CSS & JetBrains Mono Tactical UI
- **Engine:** Deterministic Algorithmic Scoring (Algo v16.1)
- **Database:** Redis/Local Vault untuk Rule Management
- **Hardware Integration:** Optimized for **AMD Instinct/Radeon** environments via ROCm.

## 🚦 Cara Menjalankan
1. Clone repositori ini.
2. Jalankan server backend: `python manage.py runserver`
3. Akses **Tactical Dashboard** di `http://localhost:8000/dashboard`
4. Konfigurasikan **Neural Bridge** ke target AI Anda (Ollama/OpenAI).
5. Aktifkan **Shield Sensitivity**.

## 📊 Roadmap
- [x] v16.1: Deterministic Engine & Tactical UI
- [ ] v16.5: Automated IP Blackholing
- [ ] v17.0: Multi-node Neural Bridge Load Balancing

---
**Developed for the AMD & LabLab.ai AI Hackathon.**
*Securing the Brain of Artificial Intelligence.*
