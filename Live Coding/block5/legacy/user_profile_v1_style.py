# -*- coding: utf-8 -*-
"""
Legacy-Beispiel: Pydantic-v1-Stil (vor Version 2.0).
"""

from pydantic import BaseModel, validator


class UserProfile(BaseModel):
    username: str
    age: int
    email: str

    class Config:
        anystr_strip_whitespace = True

    @validator("age")
    def age_must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError("age must not be negative")
        return value

    @validator("email")
    def email_must_contain_at(cls, value):
        if "@" not in value:
            raise ValueError("email must contain '@'")
        return value
