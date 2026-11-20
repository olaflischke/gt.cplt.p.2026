from pydantic import BaseModel, ConfigDict, field_validator


class UserProfile(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str
    age: int
    email: str

    @field_validator("age")
    @classmethod
    def age_must_be_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("age must not be negative")
        return value

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email must contain '@'")
        return value
