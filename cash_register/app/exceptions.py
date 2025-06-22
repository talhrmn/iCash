from fastapi import status

from shared.exceptions import iCashException


class ProductNotFoundError(iCashException):
    """Product not found in database"""

    def __init__(
            self,
            message: str = "Product not found",
            error_code: str = "PRODUCT_NOT_FOUND"
    ):
        super().__init__(message, error_code, status_code=status.HTTP_404_NOT_FOUND)


class BranchNotFoundError(iCashException):
    """Branch not found in database"""

    def __init__(
            self,
            message: str = "Branch not found",
            error_code: str = "BRANCH_NOT_FOUND"
    ):
        super().__init__(message, error_code, status_code=status.HTTP_404_NOT_FOUND)


class UserNotFoundError(iCashException):
    """User not found in database"""

    def __init__(
            self,
            message: str = "User not found",
            error_code: str = "USER_NOT_FOUND"
    ):
        super().__init__(message, error_code, status_code=status.HTTP_404_NOT_FOUND)


class PurchaseCreationError(iCashException):
    """Error creating purchase"""

    def __init__(
            self,
            message: str = "Error creating purchase",
            error_code: str = "PURCHASE_CREATION_ERROR"
    ):
        super().__init__(message, error_code, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InvalidPurchaseDataError(iCashException):
    """Invalid purchase data provided"""

    def __init__(
            self,
            message: str = "Invalid purchase data",
            error_code: str = "INVALID_PURCHASE_DATA"
    ):
        super().__init__(message, error_code, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
