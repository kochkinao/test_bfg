from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from test_task.infrastructure.in_memory import InMemoryJobRepository
from test_task.api.routes import router
from test_task.domain.exceptions import InvalidJobDataError, InvalidStatusTransitionError, JobNotFoundError

app = FastAPI()

app.state.job_repository = InMemoryJobRepository()
app.include_router(router)


@app.exception_handler(JobNotFoundError)
def job_not_found_handler(
    request: Request,
    exc: JobNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


@app.exception_handler(InvalidStatusTransitionError)
def invalid_transition_handler(
    request: Request,
    exc: InvalidStatusTransitionError,
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidJobDataError)
def invalid_job_data_handler(request: Request, exc: InvalidJobDataError):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )