from pydantic import BaseModel


class chat(BaseModel):
    input: str
    id: str

