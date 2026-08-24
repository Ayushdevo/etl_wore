"""
Custom exception hierarchy for etl_wore.
"""

class EtlException(Exception):
    """Base exception for all ETL errors."""
    pass

class ExtractionError(EtlException):
    """Raised when data extraction fails."""
    pass

class TransformationError(EtlException):
    """Raised when data transformation or validation fails."""
    pass

class LoadingError(EtlException):
    """Raised when loading data into target sinks fails."""
    pass

class ConfigurationError(EtlException):
    """Raised when configuration parameters are invalid."""
    pass
