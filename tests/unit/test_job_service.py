import pytest

from test_task.infrastructure.in_memory import InMemoryJobRepository
from test_task.services.job_services import JobService
from test_task.domain.models import JobStatus
from test_task.domain.exceptions import InvalidJobDataError, InvalidStatusTransitionError, JobNotFoundError


def test_create_job():
    repository = InMemoryJobRepository()
    service = JobService(repository)
    job = service.create_job("Собрать заказ")

    assert job.title == "Собрать заказ"
    assert job.status == JobStatus.CREATED
    assert job.assignee is None
    assert job.history == []


def test_create_job_with_empty_title():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    with pytest.raises(InvalidJobDataError):
        service.create_job("  ")


def test_job_happy_path():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    job = service.create_job("Собрать заказ")
    job = service.assign(job.id, "Alex")

    assert job.status == JobStatus.ASSIGNED
    assert job.assignee == "Alex"

    job = service.change_status(job.id, JobStatus.IN_PROGRESS)

    assert job.status == JobStatus.IN_PROGRESS

    job = service.change_status(job.id, JobStatus.COMPLETED)

    assert job.status == JobStatus.COMPLETED
    assert len(job.history) == 3


def test_invalid_transitions():
    repository = InMemoryJobRepository()
    service = JobService(repository)
    job = service.create_job("Собрать заказ")

    with pytest.raises(InvalidStatusTransitionError):
        service.change_status(job.id, JobStatus.COMPLETED)
        
    with pytest.raises(InvalidStatusTransitionError):
        service.change_status(job.id, JobStatus.IN_PROGRESS)

    with pytest.raises(InvalidStatusTransitionError):
        service.change_status(job.id, JobStatus.ON_HOLD)


def test_get_job():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    with pytest.raises(JobNotFoundError):
        service.get_job("not-found-id")


def test_change_status():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    with pytest.raises(JobNotFoundError):
        service.change_status("not-found-id", JobStatus.IN_PROGRESS)


def test_list_jobs():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    job1 = service.create_job("Задание 1")
    job2 = service.create_job("Задание 2")
    job3 = service.create_job("Задание 3")

    service.assign(job2.id, "Alex")

    all_jobs = service.list_jobs()
    created_jobs = service.list_jobs(JobStatus.CREATED)
    assigned_jobs = service.list_jobs(JobStatus.ASSIGNED)

    assert len(all_jobs) == 3
    assert len(created_jobs) == 2
    assert len(assigned_jobs) == 1