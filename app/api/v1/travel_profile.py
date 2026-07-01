import logging
from fastapi import APIRouter, Depends
from app.core.security import validate_api_key
from app.schemas.travel_profile import TravelProfileRequest, TravelProfileResponse
from app.services.profile_classifier import classify_travel_profile

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/classify", response_model=TravelProfileResponse)
def classify_profile(
    request: TravelProfileRequest,
    _: str = Depends(validate_api_key)
):
    logger.info("Classificando o perfil de viagem por preferências=%s", request.preferencias)
    return classify_travel_profile(request)
