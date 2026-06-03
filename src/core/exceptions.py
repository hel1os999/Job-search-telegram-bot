class AppError(Exception):
    """Base application error."""


class NotFoundError(AppError):
    """Entity not found."""


class ExternalServiceError(AppError):
    """Third-party API failure (HH, AI provider, etc.)."""


class AIServiceError(ExternalServiceError):
    """LLM provider error."""


class JobSourceError(ExternalServiceError):
    """Job board API error."""
