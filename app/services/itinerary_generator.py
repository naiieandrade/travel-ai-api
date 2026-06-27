from app.schemas.itinerary import ItineraryGenerateRequest, ItineraryGenerateResponse, DayPlan


def generate_itinerary(request: ItineraryGenerateRequest) -> ItineraryGenerateResponse:
    roteiro = []

    for day in range(1, request.dias + 1):
        if request.perfil == "aventura":
            manha = f"Atividade ao ar livre em {request.destino}, priorizando {request.preferencias[0]}."
            tarde = "Visita a ponto natural ou mirante, com pausa para descanso."
            noite = "Jantar leve e planejamento da atividade do dia seguinte."
        elif request.perfil == "cultural":
            manha = f"Visita a museu, centro histórico ou ponto cultural em {request.destino}."
            tarde = "Caminhada por região tradicional e pontos arquitetônicos."
            noite = "Experiência cultural, restaurante típico ou evento local."
        elif request.perfil == "gastronômica":
            manha = "Café da manhã em local tradicional."
            tarde = f"Roteiro gastronômico em {request.destino}, incluindo sabores locais."
            noite = "Jantar em restaurante recomendado da região."
        elif request.perfil == "relaxamento":
            manha = "Manhã livre para descanso."
            tarde = "Passeio leve, praia, spa ou atividade de baixa intensidade."
            noite = "Jantar tranquilo próximo à hospedagem."
        else:
            manha = f"Passeio personalizado em {request.destino}."
            tarde = "Atividade alinhada às preferências informadas."
            noite = "Tempo livre para explorar a cidade."

        roteiro.append(DayPlan(dia=day, manha=manha, tarde=tarde, noite=noite))

    return ItineraryGenerateResponse(
        destino=request.destino,
        perfil=request.perfil,
        dias=request.dias,
        roteiro=roteiro
    )
