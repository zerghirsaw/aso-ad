import numpy as np

class DALAnalyzer:
    def analyze(self, raw_data):
        data = np.asarray(raw_data, dtype=float)
        mean = np.mean(data)
        if mean == 0: return 0.01

        # 1. Coefficient of Variation (Tingkat Volatilitas)
        # Fluktuasi normal akan menghasilkan CV rendah. 
        # Lonjakan gila-gilaan (10% ke 99%) akan membuat CV meroket.
        cv = np.std(data) / mean

        # 2. Pola Asimetris Maksimal (Mencari paku/spike tertinggi)
        std = np.std(data) + 1e-8
        asym = np.abs(data - mean) / std
        max_asym = np.max(asym)

        # 3. Kalkulasi Ancaman Gabungan
        raw_score = (cv * 0.6) + (max_asym * 0.2)

        return float(np.clip(raw_score, 0.01, 1.0))
