import os
import pytest


@pytest.fixture()
def db_url():
    return os.environ['DATABASE_URL']


def test_os_env(db_url):
    assert db_url is not None


def test_postgres(db_url):
    assert "postgres" in db_url


