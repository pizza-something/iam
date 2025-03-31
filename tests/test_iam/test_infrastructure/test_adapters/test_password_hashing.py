from pytest import fixture

from iam.entities.access.password import Password
from iam.infrastructure.adapters.password_hashing import BcryptPasswordHashing


@fixture
def hashing() -> BcryptPasswordHashing:
    return BcryptPasswordHashing()


@fixture
def pasword1() -> Password:
    return Password(text="1_12345678")


@fixture
def pasword2() -> Password:
    return Password(text="2_12345678")


def test_is_hash_valid_true(
    hashing: BcryptPasswordHashing, pasword1: Password
) -> None:
    pasword1_hash = hashing.hash_of(pasword1)

    assert hashing.is_hash_valid(pasword1_hash, password=pasword1)


def test_is_hash_valid_false(
    hashing: BcryptPasswordHashing, pasword1: Password, pasword2: Password
) -> None:
    pasword1_hash = hashing.hash_of(pasword1)

    assert not hashing.is_hash_valid(pasword1_hash, password=pasword2)
