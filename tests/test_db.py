import os
import pytest


@pytest.fixture()
def project_id():
    return os.environ["GOOGLE_CLOUD_PROJECT"]


def test_os_env(project_id):
    assert project_id is not None
