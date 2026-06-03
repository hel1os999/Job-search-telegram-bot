"""Rate limiting middleware — extend when traffic grows."""

from collections import defaultdict
from time import monotonic

from telegram import Update
from telegram.ext import ContextTypes


class ThrottleMiddleware:
    def __init__(self, cooldown_seconds: float = 1.0) -> None:
        self._cooldown = cooldown_seconds
        self._last_seen: dict[int, float] = defaultdict(float)

    async def __call__(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        next_handler,
    ) -> None:
        user = update.effective_user
        if user:
            now = monotonic()
            if now - self._last_seen[user.id] < self._cooldown:
                return
            self._last_seen[user.id] = now
        await next_handler(update, context)
