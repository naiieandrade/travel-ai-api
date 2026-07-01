import logging

from app.core.config import settings
from app.schemas.itinerary import ItineraryValidateRequest, ItineraryValidateResponse
from app.services.llm_service import call_ollama_json

logger = logging.getLogger(__name__)


def validate_itinerary(request: ItineraryValidateRequest) -> ItineraryValidateResponse:
    if settings.USE_LLM:
        try:
            return validate_with_llm(request)
        except Exception as error:
            logger.warning("Fallback acionado: validação por regras. Erro: %s", error)

    return validate_with_rules(request)


def validate_with_llm(request: ItineraryValidateRequest) -> ItineraryValidateResponse:
    roteiro_texto = "\n".join(
        [
            f"Dia {dia.dia}: manhã: {dia.manha}; tarde: {dia.tarde}; noite: {dia.noite}"
            for dia in request.roteiro
        ]
    )

    prompt = f"""
Você é um especialista em turismo e planejamento de viagens.

Analise se o roteiro abaixo é viável.

Dados da viagem:
- Destino: {request.destino}
- Dias: {request.dias}
- Perfil do viajante: {request.perfil}
- Ritmo desejado: {request.ritmo}

Roteiro:
{roteiro_texto}

Avalie:
- quantidade de atividades por dia
- compatibilidade com o perfil do viajante
- compatibilidade com o ritmo informado
- possíveis problemas logísticos
- excesso de deslocamentos
- necessidade de ajustes

Responda somente em JSON válido, sem markdown, neste formato:

{{
  "viavel": true,
  "problemas": [],
  "sugestoes": [],
  "score_viabilidade": 0.9
}}

Regras:
- "viavel" deve ser true ou false
- "problemas" deve ser uma lista de textos
- "sugestoes" deve ser uma lista de textos
- "score_viabilidade" deve ser um número entre 0 e 1
"""

    data = call_ollama_json(prompt)

    return ItineraryValidateResponse(
        viavel=data["viavel"],
        problemas=data.get("problemas", []),
        sugestoes=data.get("sugestoes", []),
        score_viabilidade=data["score_viabilidade"],
    )


def validate_with_rules(request: ItineraryValidateRequest) -> ItineraryValidateResponse:
    problemas = []
    sugestoes = []

    if len(request.roteiro) != request.dias:
        problemas.append("A quantidade de dias no roteiro não corresponde ao número de dias informado.")
        sugestoes.append("Ajustar o roteiro para conter exatamente a quantidade de dias da viagem.")

    score = max(0.0, round(1 - (len(problemas) * 0.25), 2))

    return ItineraryValidateResponse(
        viavel=len(problemas) == 0,
        problemas=problemas,
        sugestoes=sugestoes,
        score_viabilidade=score,
    )