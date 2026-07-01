import logging
from app.core.config import settings
from app.schemas.itinerary import ItineraryGenerateRequest, ItineraryGenerateResponse, DayPlan
from app.services.llm_service import call_ollama_json

logger = logging.getLogger(__name__)


def generate_itinerary(request: ItineraryGenerateRequest) -> ItineraryGenerateResponse:
    if settings.USE_LLM:
        try:
            return generate_with_llm(request)
        except Exception:
            logger.warning("Fallback acionado: geração por template.")

    return generate_with_template(request)


def generate_with_llm(request: ItineraryGenerateRequest) -> ItineraryGenerateResponse:
    prompt = f"""
Você é um especialista em roteiros de viagem.

Crie um roteiro realista e personalizado.

Dados da viagem:
- Destino: {request.destino}
- Quantidade de dias: {request.dias}
- Perfil: {request.perfil}
- Orçamento: {request.orcamento}
- Preferências: {", ".join(request.preferencias)}
- Ritmo: {request.ritmo}

Regras obrigatórias:
- Responda somente em JSON válido.
- Não use markdown.
- Não use valores genéricos como "texto curto".
- Cada campo manha, tarde e noite deve conter uma sugestão específica.
- A lista roteiro deve ter exatamente {request.dias} dias.

Formato obrigatório:
{{
  "destino": "{request.destino}",
  "perfil": "{request.perfil}",
  "dias": {request.dias},
  "roteiro": [
    {{
      "dia": 1,
      "manha": "Visita a uma atração específica do destino",
      "tarde": "Atividade complementar específica",
      "noite": "Sugestão específica para a noite"
    }}
  ]
}}
"""

    data = call_ollama_json(prompt)

    return ItineraryGenerateResponse(
        destino=data["destino"],
        perfil=data["perfil"],
        dias=data["dias"],
        roteiro=[DayPlan(**item) for item in data["roteiro"]]
    )


def generate_with_template(request: ItineraryGenerateRequest) -> ItineraryGenerateResponse:
    roteiro = []

    for day in range(1, request.dias + 1):
        roteiro.append(
            DayPlan(
                dia=day,
                manha=f"Passeio em {request.destino} focado em {request.preferencias[0]}.",
                tarde="Atividade complementar alinhada ao perfil da viagem.",
                noite="Jantar e tempo livre para descanso."
            )
        )

    return ItineraryGenerateResponse(
        destino=request.destino,
        perfil=request.perfil,
        dias=request.dias,
        roteiro=roteiro
    )