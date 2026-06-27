from app.schemas.travel_profile import TravelProfileRequest, TravelProfileResponse

PROFILE_KEYWORDS = {
    "aventura": ["trilha", "trilhas", "rapel", "cachoeira", "cachoeiras", "mergulho", "escalada", "mirante"],
    "relaxamento": ["spa", "descanso", "praia", "resort", "massagem", "piscina"],
    "cultural": ["museu", "história", "historico", "cultura", "teatro", "arquitetura"],
    "gastronômica": ["gastronomia", "restaurante", "vinho", "culinária", "bar", "cafés"],
    "urbana": ["shopping", "vida noturna", "cidade", "bares", "evento", "show"],
    "família": ["crianças", "parque", "família", "zoológico", "aquário"]
}


def classify_travel_profile(request: TravelProfileRequest) -> TravelProfileResponse:
    text = " ".join(request.preferencias).lower()
    scores = {}

    for profile, keywords in PROFILE_KEYWORDS.items():
        scores[profile] = sum(1 for keyword in keywords if keyword in text)

    if request.ritmo == "intenso":
        scores["aventura"] += 1
    elif request.ritmo == "leve":
        scores["relaxamento"] += 1

    if request.companhia == "familia":
        scores["família"] += 1

    best_profile = max(scores, key=scores.get)
    total = sum(scores.values()) or 1
    confidence = round(scores[best_profile] / total, 2)

    if scores[best_profile] == 0:
        best_profile = "personalizado"
        confidence = 0.5

    return TravelProfileResponse(
        perfil_detectado=best_profile,
        confianca=confidence,
        justificativa=f"O perfil foi classificado como {best_profile} com base nas preferências, ritmo e companhia informados."
    )
