from html import escape

from db.models.vacancy import SavedVacancy
from schemas.vacancy import ScoredVacancy


def format_vacancy_card(vacancy: ScoredVacancy) -> str:
    lines = [
        f"<b>{escape(vacancy.title)}</b>",
    ]
    if vacancy.company:
        lines.append(f"{escape(vacancy.company)}")
    if vacancy.salary:
        lines.append(f"{escape(vacancy.salary)}")
    if vacancy.location:
        lines.append(f"{escape(vacancy.location)}")
    lines.append(f"Match: {vacancy.match_score:.0f}%")
    if vacancy.ai_summary:
        lines.append(f"\n{escape(vacancy.ai_summary)}")
    lines.append(f'\n<a href="{escape(vacancy.url)}">Open vacancy</a>')
    return "\n".join(lines)


def format_saved_vacancy(vacancy: SavedVacancy) -> str:
    score = f"{vacancy.match_score:.0f}%" if vacancy.match_score else "—"
    lines = [
        f"<b>{escape(vacancy.title)}</b>",
        f"{escape(vacancy.company or '—')}",
        f"Match: {score}",
        f'\n<a href="{escape(vacancy.url)}">Open</a>',
    ]
    if vacancy.ai_summary:
        lines.insert(-1, f"\n{escape(vacancy.ai_summary)}")
    return "\n".join(lines)
