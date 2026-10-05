from fastapi import APIRouter, Depends, status

from test_task.api.dependencies import get_job_service
from test_task.api.schemas import JobCreateRequest, JobResponse
from test_task.services.job_services import JobService

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