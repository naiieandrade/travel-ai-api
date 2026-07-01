import json
import logging
import ollama
from app.core.config import settings

logger = logging.getLogger(__name__)


def call_ollama_json(prompt: str) -> dict:
    try:
        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Você responde sempre em JSON válido, sem markdown."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.2,
                "num_predict": 700
            }
        )

        content = response["message"]["content"]
        return json.loads(content)

    except Exception as error:
        logger.error("Erro ao chamar Ollama: %s", error)
        raise