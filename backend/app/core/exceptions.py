from fastapi import HTTPException, status

# Creates a consistent 404 exception for missing owned resources.
def not_found(detail: str = "Resource not found") -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

# Creates a consistent 403 exception for unauthorized resource access.
def forbidden(detail: str = "Forbidden") -> HTTPException:
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
