from schemas.user import UserProfileDTO
from services.ai.client import AIClient


def _to_str(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


class ProfileParser:
    """Uses AI to parse free-text profile descriptions."""

    def __init__(self, ai: AIClient | None = None) -> None:
        self._ai = ai or AIClient()

    async def parse(self, text: str) -> UserProfileDTO:
        if not self._ai.enabled:
            return UserProfileDTO(experience=text)

        data = await self._ai.extract_profile(text)
        return UserProfileDTO(
            skills=_to_str(data.get("skills")),
            experience=_to_str(data.get("experience")),
            desired_role=_to_str(data.get("desired_role")),
            desired_salary=data.get("desired_salary"),
            location=_to_str(data.get("location")),
        )
