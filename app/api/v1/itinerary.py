import logging
from fastapi import APIRouter, Depends
from app.core.security import validate_api_key
from app.schemas.itinerary import (
    ItineraryGenerateRequest,
    ItineraryGenerateResponse,
    ItineraryValidateRequest,
    ItineraryValidateResponse,
)
from app.services.itinerary_generator import generate_itinerary
from app.services.itinerary_validator import validate_itinerary

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=ItineraryGenerateResponse)
def generate(
    request: ItineraryGenerateRequest,
    _: str = Depends(validate_api_key)
):
    logger.info("Generating itinerary for destination=%s days=%s", request.destino, request.dias)
    return generate_itinerary(request)


@router.post("/validate", response_model=ItineraryValidateResponse)
def validate(
    request: ItineraryValidateRequest,
    _: str = Depends(validate_api_key)
):
    logger.info("Validating itinerary for destination=%s days=%s", request.destino, request.dias)
    return validate_itinerary(request)
