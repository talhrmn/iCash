from fastapi import status


class iCashException(Exception):
    """
    Base exception class for iCash system.
    Carries a message, an optional error_code, and an HTTP status_code.
    """

    def __init__(
            self,
            message: str,
            error_code: str = None,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)


class ValidationError(iCashException):
    """Data validation errors"""

    def __init__(
            self,
            message: str = "Validation error",
            error_code: str = "VALIDATION_ERROR"
    ):
        super().__init__(message, error_code, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class InsufficientDataError(ValidationError):
    """Required data is missing"""

    def __init__(
            self,
            message: str = "Required data is missing",
            error_code: str = "INSUFFICIENT_DATA"
    ):
        super().__init__(message, error_code)
        self.status_code = status.HTTP_400_BAD_REQUEST


class BusinessRuleViolationError(ValidationError):
    """Business rule validation errors"""

    def __init__(
            self,
            message: str = "Business rule violation",
            error_code: str = "BUSINESS_RULE_VIOLATION"
    ):
        super().__init__(message, error_code)
        self.status_code = status.HTTP_400_BAD_REQUEST


class InvalidBranchError(BusinessRuleViolationError):
    """Invalid branch ID - must be one of the 3 predefined branches"""

    def __init__(
            self,
            message: str = "Invalid branch ID. Must be one of: SMKT001, SMKT002, SMKT003",
            error_code: str = "INVALID_BRANCH"
    ):
        super().__init__(message, error_code)


class InvalidProductCountError(BusinessRuleViolationError):
    """System must have exactly 10 products"""

    def __init__(
            self,
            message: str = "System must have exactly 10 products",
            error_code: str = "INVALID_PRODUCT_COUNT"
    ):
        super().__init__(message, error_code)


class DuplicateProductInPurchaseError(BusinessRuleViolationError):
    """Customer can buy at most one unit of each product per purchase"""

    def __init__(
            self,
            message: str = "Customer can buy at most one unit of each product per purchase",
            error_code: str = "DUPLICATE_PRODUCT_IN_PURCHASE"
    ):
        super().__init__(message, error_code)
