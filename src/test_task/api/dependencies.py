from fastapi import Depends, Request

from test_task.domain.repository import JobRepository
from test_task.services.job_services import JobService


def get_repository(request: Request) -> JobRepository:
    return request.app.state.job_repository


def get_job_service(repository: JobRepository = Depends(get_repository)) -> JobService:
    return JobService(repository)