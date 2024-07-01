from fastapi.responses import JSONResponse

def Response(status:int=200,message:str="OK",metadata:any=None):
    return JSONResponse(
        status_code=status,
        content={
            "status":"Success",
            "message":message,
            "metadata":metadata,
        }
    )