from telegram.ext import Application

from bot.handlers.common import register_common_handlers
from bot.handlers.profile import register_profile_handlers
from bot.handlers.saved import register_saved_handlers
from bot.handlers.search import register_search_handlers
from bot.handlers.start import register_start_handlers


def register_handlers(app: Application) -> None:
    register_start_handlers(app)
    register_search_handlers(app)
    register_profile_handlers(app)
    register_saved_handlers(app)
    register_common_handlers(app)
