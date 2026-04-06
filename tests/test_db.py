import os

import pytest


@pytest.fixture()
def project_id():
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        pytest.skip("Requires GOOGLE_CLOUD_PROJECT environment variable")
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.mark.integration
def test_os_env(project_id):
    assert project_id is not None
