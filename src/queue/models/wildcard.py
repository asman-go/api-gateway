from pydantic import BaseModel, field_validator
import re


class WildcardFormatException(Exception):...


class WildcardDomain(BaseModel):
    domain: str

    @field_validator('domain')
    def address_validator(cls, value):
        if not re.fullmatch(r'[*][.][^*]+', value):
            raise WildcardFormatException

        return value
