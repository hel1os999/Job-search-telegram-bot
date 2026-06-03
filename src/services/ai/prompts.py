"""System prompts for LLM calls."""

PROFILE_EXTRACTION = """\
Extract job search profile fields from the user's message.
Return JSON with keys: skills, experience, desired_role, desired_salary, location.
Use null for missing fields. desired_salary must be an integer (USD/month) or null.
"""

VACANCY_MATCH_BATCH = """\
You are a career assistant. Given a user profile and a list of vacancies, score each one.
Return JSON object with key "results" containing an array in the same order as the input:
{"results": [{"score": 0-100, "summary": "1-2 sentences explaining fit"}, ...]}
Be concise.
"""

QUERY_REFINEMENT = """\
Improve the job search query based on the user's profile.
Return JSON: {"query": "...", "explanation": "one sentence in English"}
"""
