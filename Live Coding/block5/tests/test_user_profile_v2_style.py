import pytest
from pydantic import ValidationError

from code_examples.modernized.user_profile_v2_style import UserProfile


def test_user_profile_trims_strings_and_accepts_valid_profile():
    profile = UserProfile(
        username="  alice  ",
        age=30,
        email=" alice@example.com ",
    )

    assert profile.username == "alice"
    assert profile.email == "alice@example.com"


@pytest.mark.parametrize("age", [-1, -100])
def test_user_profile_rejects_negative_age(age):
    with pytest.raises(ValidationError):
        UserProfile(username="bob", age=age, email="bob@example.com")


def test_user_profile_accepts_zero_age():
    profile = UserProfile(username="alice", age=0, email="alice@example.com")

    assert profile.age == 0


@pytest.mark.parametrize("email", ["", "carol-example.com"])
def test_user_profile_rejects_email_without_at(email):
    with pytest.raises(ValidationError):
        UserProfile(username="carol", age=25, email=email)


def test_user_profile_rejects_number_as_username():
    with pytest.raises(ValidationError):
        UserProfile(username=123, age=30, email="dave@example.com")


def test_user_profile_rejects_fractional_age():
    with pytest.raises(ValidationError):
        UserProfile(username="alice", age=1.5, email="alice@example.com")
