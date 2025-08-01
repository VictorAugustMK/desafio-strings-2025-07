from pydantic import BaseModel, Field
from typing import Optional

class FileRequest(BaseModel):
    path: str
    width: Optional[int] = None
