from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    id: int | None = Field(default=None, description="Unique identifier for the entity")
    created_at: datetime | None = Field(default=None, description="Creation date")
    updated_at: datetime | None = Field(default=None, description="Last update date")

    model_config = ConfigDict(exclude_none=True)  # type: ignore
