class KnowledgeDomainException(Exception):
    """Base exception for knowledge domain failures."""


class KnowledgeValidationException(KnowledgeDomainException):
    """Raised when a knowledge domain object violates business rules."""


class KnowledgeDocumentNotFoundException(KnowledgeDomainException):
    """Raised when a knowledge document cannot be found."""


class KnowledgeChunkNotFoundException(KnowledgeDomainException):
    """Raised when a knowledge chunk cannot be found."""


class BusinessSummaryNotFoundException(KnowledgeDomainException):
    """Raised when a business summary cannot be found."""
