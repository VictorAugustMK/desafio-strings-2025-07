from pydantic import BaseModel, Field
from typing import Optional

class FileRequest(BaseModel):
    path: str
    width: Optional[int] = Field(40, gt=0, le=120, description="Número de caracteres por linha (1 a 120)")
