from fastapi import APIRouter, Depends, status

from test_task.api.dependencies import get_job_service
from test_task.api.schemas import JobCreateRequest, JobResponse, JobAssignRequest, JobStatusChangeRequest
from test_task.services.job_services import JobService
from test_task.domain.models import JobStatus

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED
)
def create_job(
    request: JobCreateRequest,
    service: JobService = Depends(get_job_service)
):
    job = service.create_job(request.title)

    return JobResponse.model_validate(job)


@router.get(
    "/{job_id}",
    response_model=JobResponse
)
def get_job(
    job_id: str,
    service: JobService = Depends(get_job_service)
) -> JobResponse:
    job = service.get_job(job_id)
    return JobResponse.model_validate(job)


@router.get(
    "",
    response_model=list[JobResponse]
)
def list_jobs(
    status: JobStatus | None = None,
    service: JobService = Depends(get_job_service)
) -> list[JobResponse]:
    jobs = service.list_jobs(status)

    return [JobResponse.model_validate(job) for job in jobs]


@router.post(
    "/{job_id}/assign",
    response_model=JobResponse,
)
def assign_job(
    job_id: str,
    request: JobAssignRequest,
    service: JobService = Depends(get_job_service),
) -> JobResponse:
    job = service.assign(job_id, request.assignee)

    return JobResponse.model_validate(job)


@router.post(
    "/{job_id}/status",
    response_model=JobResponse,
)
def change_job_status(
    job_id: str,
    request: JobStatusChangeRequest,
    service: JobService = Depends(get_job_service),
) -> JobResponse:
    job = service.change_status(job_id, request.new_status)

    return JobResponse.model_validate(job)