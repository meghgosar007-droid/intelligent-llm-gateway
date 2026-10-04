from dataclasses import dataclass


@dataclass
class ModelInfo:
    name: str
    provider: str
    cost_per_1k_tokens: float
    quality: int

gemini_flash = ModelInfo(
    name="gemini-3.8-flash",
    provider="google",
    cost_per_1k_tokens=0.001,
    quality=7
)