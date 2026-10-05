from test_task.infrastructure.in_memory import InMemoryJobRepository
from test_task.services.job_services import JobService
from test_task.domain.models import JobStatus


def test_create_job():
    repository = InMemoryJobRepository()
    service = JobService(repository)
    job = service.create_job("Собрать заказ")

    assert job.title == "Собрать заказ"
    assert job.status == JobStatus.CREATED
    assert job.assignee is None
    assert job.history == []