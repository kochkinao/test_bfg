from app.domain.repository import JobRepository
from app.domain.models import Job, JobStatus
from app.domain.exceptions import InvalidJobDataError

from uuid import uuid4
from datetime import datetime, timezone




class JobService:
    def __init__(self, repository: JobRepository):
        self._repository = repository

    def create_job(self, title: str) -> Job:
        if not title.strip():
            raise InvalidJobDataError("Название задания не может быть пустым")

        now = datetime.now(timezone.utc)

        job = Job(
            id=str(uuid4()),
            title=title,
            status=JobStatus.CREATED,
            assignee=None,
            created_at=now,
            updated_at=now,
            history=[]
        )

        self._repository.save(job)

        return job