from app.schemas.itinerary import ItineraryValidateRequest, ItineraryValidateResponse

INTENSE_ACTIVITIES = ["trilha", "rapel", "escalada", "mergulho", "cachoeira", "pedra", "montanha"]


def validate_itinerary(request: ItineraryValidateRequest) -> ItineraryValidateResponse:
    problemas = []
    sugestoes = []

    activities_per_day = len(request.atividades) / request.dias

    if activities_per_day > 4:
        problemas.append("O roteiro possui muitas atividades por dia.")
        sugestoes.append("Reduzir a quantidade de atividades ou aumentar o número de dias.")

    intense_count = sum(
        1 for activity in request.atividades
        if any(keyword in activity.lower() for keyword in INTENSE_ACTIVITIES)
    )

    if request.ritmo == "leve" and intense_count >= 2:
        problemas.append("O ritmo leve parece incompatível com a quantidade de atividades intensas.")
        sugestoes.append("Trocar parte das atividades intensas por passeios leves.")

    if request.perfil == "relaxamento" and intense_count >= 2:
        problemas.append("O perfil de relaxamento não está alinhado com várias atividades de aventura.")
        sugestoes.append("Adicionar mais períodos livres ou atividades de descanso.")

    if request.dias == 1 and len(request.atividades) > 3:
        problemas.append("Um dia pode ser insuficiente para executar todas as atividades.")
        sugestoes.append("Priorizar no máximo três atividades principais.")

    score = max(0.0, round(1 - (len(problemas) * 0.25), 2))

    return ItineraryValidateResponse(
        viavel=len(problemas) == 0,
        problemas=problemas,
        sugestoes=sugestoes,
        score_viabilidade=score
    )
