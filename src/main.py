"""Entry point: python -m job_search"""

from bot.app import create_application
from core.config import settings
from core.logging import setup_logging


def main() -> None:
    setup_logging(settings.log_level)
    create_application().run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
