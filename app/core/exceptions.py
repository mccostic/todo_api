class AppException(Exception):
    def __init__(self, message: str, code: int, details: str = None):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(self.message)

# ─── Network ──────────────────────────────────
class NetworkException(AppException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Network error occurred",
            code=1000,
            details=details,
        )

# ─── Server ───────────────────────────────────
class ServerException(AppException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Server error occurred",
            code=2000,
            details=details,
        )

class UnauthorizedException(AppException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Unauthorized - Invalid API key",
            code=2001,
            details=details,
        )

class ForbiddenException(AppException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Forbidden - Access denied",
            code=2002,
            details=details,
        )

class NotFoundException(AppException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Resource not found",
            code=2003,
            details=details,
        )

class ConflictException(AppException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Resource already exists",
            code=2004,
            details=details,
        )

class ValidationException(AppException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Validation failed",
            code=2005,
            details=details,
        )

class RateLimitException(AppException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Too many requests",
            code=2006,
            details=details,
        )

# ─── Business ─────────────────────────────────
class BusinessException(AppException):
    def __init__(self, message: str, code: int, details: str = None):
        super().__init__(message=message, code=code, details=details)

class TodoNotFoundException(BusinessException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Todo not found",
            code=3001,
            details=details,
        )

class TodoAlreadyCompletedException(BusinessException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Todo is already completed",
            code=3002,
            details=details,
        )

class TodoTitleEmptyException(BusinessException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Todo title cannot be empty",
            code=3003,
            details=details,
        )

class TodoLimitExceededException(BusinessException):
    def __init__(self, details: str = None):
        super().__init__(
            message="Maximum todo limit reached",
            code=3004,
            details=details,
        )