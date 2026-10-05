from test_task.domain.models import JobStatus
from datetime import datetime

from pydantic import BaseModel, ConfigDict

class JobCreateRequest(BaseModel):
    title: str


class JobAssignRequest(BaseModel):
    assignee: str


class JobStatusChangeRequest(BaseModel):
    new_status: JobStatus


class JobHistoryEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    from_status: JobStatus
    to_status: JobStatus
    changed_at: datetime


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    status: JobStatus
    assignee: str | None
    created_at: datetime
    updated_at: datetime
    history: list[JobHistoryEntryResponse]