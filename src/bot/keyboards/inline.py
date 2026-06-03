from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def vacancy_actions_keyboard(vacancy_id: str, source: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Save",
                    callback_data=f"save:{source}:{vacancy_id}",
                ),
            ],
        ]
    )


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Search", callback_data="menu:search"),
                InlineKeyboardButton("Profile", callback_data="menu:profile"),
            ],
            [
                InlineKeyboardButton("Saved", callback_data="menu:saved"),
            ],
        ]
    )
