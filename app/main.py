from fastapi import FastAPI
from app.api.v1 import travel_profile, itinerary
from app.core.logging_config import configure_logging

configure_logging()

app = FastAPI(
    title="Polaris Travel AI API",
    description="API inteligente para geração e validação de roteiros de viagem.",
    version="1.0.0"
)

app.include_router(travel_profile.router, prefix="/api/v1/travel-profile", tags=["Travel Profile"])
app.include_router(itinerary.router, prefix="/api/v1/itinerary", tags=["Itinerary"])


@app.get("/")
def root():
    return {"message": "Polaris Travel AI API is running"}
