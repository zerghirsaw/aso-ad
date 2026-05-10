import torch

class AntiDistillation:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def apply_perturbation(self, score):
        # Placeholder logits (saran optimasi sistem)
        logits = torch.tensor([1.5, -0.5, 3.0, 0.2]).to(self.device)
        noise = torch.randn_like(logits) * (score * 2.0 if score > 0.5 else 0.01)
        return (logits + noise).cpu().tolist()
