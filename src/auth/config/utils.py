from starlette.responses import JSONResponse


def error_info():
    return JSONResponse(status_code=404, content={'Message': 'Sorry, something went wrong, try again later'})
