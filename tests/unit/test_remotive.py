import pytest
from services.sources.remotive import RemotiveSource


@pytest.fixture
def source() -> RemotiveSource:
    return RemotiveSource()


def _raw_job(**kwargs) -> dict:
    base = {
        "id": 42,
        "title": "Senior Python Developer",
        "company_name": "TechCorp",
        "url": "https://remotive.com/job/42",
        "salary": "$4000 - $6000",
        "candidate_required_location": "Worldwide",
        "publication_date": "2026-05-31T00:00:00",
    }
    base.update(kwargs)
    return base


def test_map_item_basic(source):
    job = source._map_item(_raw_job())
    assert job.external_id == "42"
    assert job.source == "remotive"
    assert job.title == "Senior Python Developer"
    assert job.company == "TechCorp"
    assert job.url == "https://remotive.com/job/42"
    assert job.salary == "$4000 - $6000"
    assert job.location == "Worldwide"


def test_map_item_empty_salary(source):
    job = source._map_item(_raw_job(salary=""))
    assert job.salary is None


def test_map_item_missing_optional_fields(source):
    job = source._map_item(_raw_job(salary=None, candidate_required_location=None))
    assert job.salary is None
    assert job.location is None


def test_map_item_id_is_string(source):
    job = source._map_item(_raw_job(id=9999))
    assert isinstance(job.external_id, str)
    assert job.external_id == "9999"
