from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class JobStatus(str, Enum):
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ON_HOLD = "ON_HOLD"


@dataclass
class JobHistoryEntry:
    from_status: JobStatus
    to_status: JobStatus
    changed_at: datetime


@dataclass
class Job:
    id: str
    title: str
    status: JobStatus
    assignee: str | None
    created_at: datetime
    updated_at: datetime
    history: list[JobHistoryEntry]


JOB_STATUS_TRANSITIONS: dict[JobStatus, set[JobStatus]] = {
    JobStatus.CREATED: {
        JobStatus.ASSIGNED,
        JobStatus.CANCELLED
    },
    JobStatus.IN_PROGRESS: {
        JobStatus.CANCELLED,
        JobStatus.ON_HOLD,
        JobStatus.COMPLETED
    },
    JobStatus.ON_HOLD: {
        JobStatus.IN_PROGRESS
    },
    JobStatus.ASSIGNED: {
        JobStatus.CANCELLED,
        JobStatus.IN_PROGRESS
    },
    JobStatus.COMPLETED: set(),
    JobStatus.CANCELLED: set()
}