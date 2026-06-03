import json
import logging
from typing import Any

import httpx

from core.config import settings
from core.exceptions import AIServiceError
from services.ai import prompts

logger = logging.getLogger(__name__)


def _extract_list(value: Any) -> list[dict[str, Any]]:
    """Normalize AI response to a flat list of dicts regardless of wrapping."""
    if isinstance(value, list):
        # unwrap [[...]] → [...]
        if value and isinstance(value[0], list):
            value = value[0]
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        for key in ("results", "vacancies", "scores", "items"):
            if key in value and isinstance(value[key], list):
                return _extract_list(value[key])
    return []


class AIClient:
    """Thin wrapper over OpenAI-compatible chat completions API."""

    def __init__(self) -> None:
        self._enabled = settings.ai.api_key is not None

    @property
    def enabled(self) -> bool:
        return self._enabled

    async def _chat(self, system: str, user: str) -> str:
        if not self._enabled:
            raise AIServiceError("AI is not configured (set APP_CONFIG__AI__API_KEY)")

        headers = {
            "Authorization": f"Bearer {settings.ai.api_key.get_secret_value()}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.ai.model,
            "max_tokens": settings.ai.max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
        }

        async with httpx.AsyncClient(
            base_url=settings.ai.base_url,
            timeout=60.0,
        ) as client:
            try:
                response = await client.post("/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
            except httpx.HTTPError as exc:
                logger.exception("AI request failed")
                raise AIServiceError(str(exc)) from exc

        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def _json_chat(self, system: str, user: str) -> dict[str, Any]:
        raw = await self._chat(system, user)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AIServiceError(f"Invalid JSON from AI: {raw[:200]}") from exc

    async def extract_profile(self, text: str) -> dict[str, Any]:
        return await self._json_chat(prompts.PROFILE_EXTRACTION, text)

    async def score_vacancies_batch(self, profile_context: str, vacancies_text: str) -> list[dict[str, Any]]:
        user = f"Profile:\n{profile_context}\n\nVacancies:\n{vacancies_text}"
        result = await self._json_chat(prompts.VACANCY_MATCH_BATCH, user)
        if isinstance(result, dict):
            return _extract_list(result.get("results", result))
        return _extract_list(result)

    async def refine_query(self, profile_context: str, raw_query: str) -> dict[str, Any]:
        user = f"Profile:\n{profile_context}\n\nQuery: {raw_query}"
        return await self._json_chat(prompts.QUERY_REFINEMENT, user)
