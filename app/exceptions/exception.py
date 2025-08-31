from fastapi import status


class BusinessException(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        message: str = "Bad Request",
    ):
        self.status_code = status_code
        self.message = message


class NotFoundException(BusinessException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
        )


class AlreadyExistsException(BusinessException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
        )
