from pydantic import BaseModel, field_validator


class DomainFormatException(Exception):...


class Domain(BaseModel):
    domain: str

    @field_validator('domain')
    def address_validator(cls, value):
        if '*' in value:
            raise DomainFormatException

        return  value
