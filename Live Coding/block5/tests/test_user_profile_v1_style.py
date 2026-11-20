import pydantic
import pytest

if not pydantic.__version__.startswith("1."):
    pytest.skip("Pydantic v1 baseline only", allow_module_level=True)

from pydantic import ValidationError

from legacy.user_profile_v1_style import UserProfile


@pytest.mark.parametrize(
    ("username", "email"),
    [
        ("  alice  ", " alice@example.com "),
        ("bob", "bob@example.com"),
    ],
)
def test_user_profile_trims_strings_and_accepts_valid_email(username, email):
    profile = UserProfile(username=username, age=30, email=email)

    assert profile.username == username.strip()
    assert profile.email == email.strip()


def test_user_profile_accepts_zero_age():
    profile = UserProfile(username="alice", age=0, email="alice@example.com")

    assert profile.age == 0


@pytest.mark.parametrize("age", [-1, -100])
def test_user_profile_rejects_negative_age(age):
    with pytest.raises(ValidationError):
        UserProfile(username="alice", age=age, email="alice@example.com")


@pytest.mark.parametrize("email", ["", "carol-example.com"])
def test_user_profile_rejects_empty_or_invalid_email(email):
    with pytest.raises(ValidationError):
        UserProfile(username="carol", age=25, email=email)


@pytest.mark.parametrize("field", ["username", "age", "email"])
def test_user_profile_rejects_none_for_required_fields(field):
    payload = {
        "username": "alice",
        "age": 30,
        "email": "alice@example.com",
    }
    payload[field] = None

    with pytest.raises(ValidationError):
        UserProfile(**payload)


def test_user_profile_coerces_numeric_username_to_string():
    profile = UserProfile(username=123, age=30, email="alice@example.com")

    assert profile.username == "123"


def test_user_profile_truncates_fractional_age():
    profile = UserProfile(username="alice", age=1.5, email="alice@example.com")

    assert profile.age == 1


def test_user_profile_accepts_large_age_without_declared_upper_bound():
    maximum_signed_64_bit_integer = 2**63 - 1
    profile = UserProfile(
        username="alice",
        age=maximum_signed_64_bit_integer,
        email="alice@example.com",
    )

    assert profile.age == maximum_signed_64_bit_integer
