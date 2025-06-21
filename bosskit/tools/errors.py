from dataclasses import dataclass
from typing import Optional


class BossKitError(Exception):
    """Base class for all BossKit errors."""
    pass

class ConfigurationError(BossKitError):
    """Raised when there is a configuration error."""
    pass

class ModelError(BossKitError):
    """Raised when there is a model-related error."""
    pass

class APIError(BossKitError):
    """Raised when there is an API-related error."""
    pass

class ValidationError(BossKitError):
    """Raised when validation fails."""
    pass

class AuthenticationError(BossKitError):
    """Raised when authentication fails."""
    pass

class RateLimitError(BossKitError):
    """Raised when rate limit is exceeded."""
    pass

class TimeoutError(BossKitError):
    """Raised when an operation times out."""
    pass

class ResourceNotFoundError(BossKitError):
    """Raised when a resource is not found."""
    pass

class InvalidOperationError(BossKitError):
    """Raised when an invalid operation is attempted."""
    pass

class UnsupportedFeatureError(BossKitError):
    """Raised when an unsupported feature is used."""
    pass

class PermissionError(BossKitError):
    """Raised when there is a permission error."""
    pass

@dataclass
class ErrorDetails:
    """Container for error details."""
    message: str
    code: Optional[str] = None
    details: Optional[dict] = None
    context: Optional[dict] = None

    def __str__(self):
        return f"Error: {self.message} (code: {self.code})"

    def to_dict(self):
        """Convert error details to dictionary."""
        return {
            'message': self.message,
            'code': self.code,
            'details': self.details,
            'context': self.context
        }

    @classmethod
    def from_exception(cls, exc: Exception):
        """Create ErrorDetails from an exception."""
        return cls(
            message=str(exc),
            code=getattr(exc, 'code', None),
            details=getattr(exc, 'details', None),
            context=getattr(exc, 'context', None)
        )

def handle_error(exc: Exception, context: Optional[dict] = None) -> ErrorDetails:
    """Handle an error and return ErrorDetails.

    Args:
        exc: Exception to handle
        context: Additional context information

    Returns:
        ErrorDetails object containing error information
    """
    if isinstance(exc, BossKitError):
        return ErrorDetails(
            message=str(exc),
            code=getattr(exc, 'code', None),
            details=getattr(exc, 'details', None),
            context=context or {}
        )
    else:
        return ErrorDetails(
            message=f"Unexpected error: {str(exc)}",
            code='UNKNOWN_ERROR',
            details={'original_exception': str(exc)},
            context=context or {}
        )
