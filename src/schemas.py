from pydantic import BaseModel


class Serializer(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True
