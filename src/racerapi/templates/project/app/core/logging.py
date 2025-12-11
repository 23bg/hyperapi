async def logger(request, call_next):
    print("Hit", request.url.path)
    resp = await call_next(request)
    return resp