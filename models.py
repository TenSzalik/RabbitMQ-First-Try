from pydantic import BaseModel


class EncodedMessage(BaseModel):
    message: str
