from abc import ABC, abstractmethod
from .models import Job


class JobRepository(ABC):

    @abstractmethod
    def save(self, job: Job) -> None:
        pass

    @abstractmethod
    def get(self, job_id: str) -> Job | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Job]:
        pass