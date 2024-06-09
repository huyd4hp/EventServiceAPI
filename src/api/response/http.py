from fastapi import HTTPException,status
def HTTP_204_NO_CONTENT():
    return HTTPException(
        status_code=status.HTTP_204_NO_CONTENT
    )
def HTTP_400_BAD_REQUEST(detail:any="Bad Request"):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )
def HTTP_401_UNAUTHORIZED(detail:any="Unauthoized"):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail
    )
def HTTP_403_FORBIDDEN(detail:any="Forbidden"):
    return HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = detail,
    )
def HTTP_404_NOT_FOUND(detail:any="Not Found"):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )

def HTTP_409_CONFLICT(detail:any='Conflict'):
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail
    )
def HTTP_500_INTERNAL_SERVER_ERROR(detail:any='Internal Server Error'):
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail
    )


