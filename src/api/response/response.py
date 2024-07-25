from fastapi.responses import JSONResponse

def Response(status: int = 200, message: str = "OK", metadata: any = None):
    content = {
        "status": "Success",
        "message": message,
    }
    if metadata is not None:
        content["metadata"] = metadata

    return JSONResponse(
        status_code=status,
        content=content
    )
