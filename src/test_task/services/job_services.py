from test_task.domain.repository import JobRepository
from test_task.domain.models import Job, JobStatus, JOB_STATUS_TRANSITIONS, JobHistoryEntry
from test_task.domain.exceptions import InvalidJobDataError, JobNotFoundError, InvalidStatusTransitionError

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

    def get_job(self, job_id: str) -> Job:
        job = self._repository.get(job_id)

        if job is None:
            raise JobNotFoundError(f"Задание с id={job_id} не найдено")
        
        return job

    
    def assign(self, job_id: str, assignee: str) -> Job:
        job = self.get_job(job_id)

        if JobStatus.ASSIGNED not in JOB_STATUS_TRANSITIONS[job.status]:
            raise InvalidStatusTransitionError(
                f"Недопустимый переход: {job.status.value} -> {JobStatus.ASSIGNED.value}"
            )

        old_status = job.status
        job.assignee = assignee
        job.status = JobStatus.ASSIGNED
        job.updated_at = datetime.now(timezone.utc)
        job.history.append(
            JobHistoryEntry(
                from_status=old_status,
                to_status=JobStatus.ASSIGNED,
                changed_at=job.updated_at
            )
        )

        self._repository.save(job)
        return job
        
    
    def change_status(self, job_id: str, new_status: JobStatus) -> Job:
        job = self.get_job(job_id)

        if new_status not in JOB_STATUS_TRANSITIONS[job.status]:
            raise InvalidStatusTransitionError(
                f"Недопустимый переход: {job.status.value} -> {new_status.value}"
            )

        old_status = job.status
        job.status = new_status
        job.updated_at = datetime.now(timezone.utc)
        job.history.append(
            JobHistoryEntry(
                from_status=old_status,
                to_status=new_status,
                changed_at=job.updated_at
            )
        )

        self._repository.save(job)
        return job

    
    def list_jobs(self, status: JobStatus | None = None) -> list[Job]:
        jobs = self._repository.list_all()

        if status is None:
            return jobs
        
        return [job for job in jobs if job.status == status]