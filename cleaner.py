from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal

class TexasPermit(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    permit_number: str = Field(pattern=r"^TDLR-\d{4}-\d{3}$")
    county: str = Field(min_length=1)
    trade: Literal["Electrical", "Plumbing", "Hvac"]
    contractor: str = Field(min_length=1)
    issue_date: str
    value: int = Field(gt=0)

    @field_validator('county', mode='before')
    @classmethod
    def clean_county(cls, v):
        if isinstance(v, str):
            return v.strip().title()
        return v

    @field_validator('trade', mode='before')
    @classmethod
    def clean_trade(cls, v):
        if isinstance(v, str):
            return v.strip().title()
        return v

    @field_validator('contractor', mode='before')
    @classmethod
    def clean_contractor(cls, v):
        if isinstance(v, str):
            return v.strip().title()
        return v