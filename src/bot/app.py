from telegram.ext import Application

from bot.handlers import register_handlers
from core.config import settings
from core.container import container


def create_application() -> Application:
    app = (
        Application.builder()
        .token(settings.bot.token.get_secret_value())
        .build()
    )
    app.bot_data["container"] = container
    register_handlers(app)
    return app
