from starlette import status

from shared.exceptions import iCashException


class DatabaseError(iCashException):
    """Database operation errors"""

    def __init__(
            self,
            message: str = "Database operation error",
            error_code: str = "DATABASE_ERROR"
    ):
        super().__init__(message, error_code, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
