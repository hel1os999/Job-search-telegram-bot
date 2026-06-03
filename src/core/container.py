"""Simple dependency container — wires services for handlers."""

from dataclasses import dataclass, field

from db.repositories.search_repo import SearchRepository
from db.repositories.user_repo import UserRepository
from db.repositories.vacancy_repo import VacancyRepository
from db.session import db_helper
from services.ai.client import AIClient
from services.sources.aggregator import JobSearchAggregator
from services.matching.scorer import VacancyScorer


@dataclass
class Container:
    ai_client: AIClient = field(default_factory=AIClient)
    job_search: JobSearchAggregator = field(default_factory=JobSearchAggregator)
    vacancy_scorer: VacancyScorer = field(default_factory=VacancyScorer)

    @property
    def session_factory(self):
        return db_helper.session_factory

    def users(self, session):
        return UserRepository(session)

    def searches(self, session):
        return SearchRepository(session)

    def vacancies(self, session):
        return VacancyRepository(session)


container = Container()
