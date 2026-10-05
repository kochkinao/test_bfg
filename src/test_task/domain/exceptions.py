

class JobServiceError(Exception):
    pass


class JobNotFoundError(JobServiceError):
    pass


class InvalidStatusTransitionError(JobServiceError):
    pass


class InvalidJobDataError(JobServiceError):
    pass