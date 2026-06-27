from typing import List
from pydantic import BaseModel, Field


class TravelProfileRequest(BaseModel):
    preferencias: List[str] = Field(..., min_length=1, examples=[["trilhas", "cachoeiras", "rapel"]])
    ritmo: str = Field(..., examples=["leve", "moderado", "intenso"])
    orcamento: str = Field(..., examples=["baixo", "medio", "alto"])
    companhia: str = Field(..., examples=["solo", "casal", "familia", "amigos"])


class TravelProfileResponse(BaseModel):
    perfil_detectado: str
    confianca: float
    justificativa: str
