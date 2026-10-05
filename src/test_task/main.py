from fastapi import FastAPI
from test_task.infrastructure.in_memory import InMemoryJobRepository

app = FastAPI()

app.state.job_repository = InMemoryJobRepository()