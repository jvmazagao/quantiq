from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    id: str

    model_config = ConfigDict(exclude_none=True)  # type: ignore
