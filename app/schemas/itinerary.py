from typing import List
from pydantic import BaseModel, Field


class ItineraryGenerateRequest(BaseModel):
    destino: str = Field(..., min_length=2, examples=["Chapada dos Veadeiros"])
    dias: int = Field(..., ge=1, le=30, examples=[4])
    perfil: str = Field(..., examples=["aventura"])
    orcamento: str = Field(..., examples=["medio"])
    preferencias: List[str] = Field(..., min_length=1, examples=[["trilhas", "cachoeiras", "gastronomia local"]])
    ritmo: str = Field(..., examples=["leve", "moderado", "intenso"])


class DayPlan(BaseModel):
    dia: int
    manha: str
    tarde: str
    noite: str


class ItineraryGenerateResponse(BaseModel):
    destino: str
    dias: int
    perfil: str
    ritmo: str
    roteiro: List[DayPlan]


class ItineraryValidateRequest(BaseModel):
    destino: str = Field(..., examples=["Rio de Janeiro"])
    dias: int = Field(..., ge=1, le=30, examples=[2])
    perfil: str = Field(..., examples=["aventura"])
    ritmo: str = Field(..., examples=["intenso"])
    roteiro: List[DayPlan] = Field(..., min_length=1)


class ItineraryValidateResponse(BaseModel):
    viavel: bool
    problemas: List[str]
    sugestoes: List[str]
    score_viabilidade: float
