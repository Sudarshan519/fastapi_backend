from functools import wraps

from fastapi import FastAPI, Request
from pydantic import BaseModel
def auth_required(handler):
    @wraps(handler)
    async def wrapper(request: Request,*args, **kwargs):
        return await handler(*args, **kwargs)

    return wrapper