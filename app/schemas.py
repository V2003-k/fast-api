from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class config:
        orm_mode = True
        # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict

