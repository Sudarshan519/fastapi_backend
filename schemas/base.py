from datetime import date
from typing import Optional, TypeVar, Generic, List

from fastapi import HTTPException
from pydantic import BaseModel, validator
from pydantic.generics import GenericModel
T = TypeVar('T')

class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None


class PageResponse(BaseModel):
    """ The response for a pagination query. """
    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]

