from pydantic import BaseModel
from test_task.domain.models import JobStatus
from datetime import datetime


class JobCreateRequest(BaseModel):
    title: str


class JobHistoryEntryResponse(BaseModel):
    from_status: JobStatus
    to_status: JobStatus
    changed_at: datetime


class JobResponse(BaseModel):
    id: str
    title: str
    status: JobStatus
    assignee: str | None
    created_at: datetime
    updated_at: datetime
    history: list[JobHistoryEntryResponse]


class JobAssignRequest(BaseModel):
    assignee: str


class JobStatusChangeRequest(BaseModel):
    new_status: JobStatus