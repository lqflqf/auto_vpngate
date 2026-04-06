import os

import pytest

import configuration


@pytest.fixture
def config_obj():
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        pytest.skip("Requires GOOGLE_CLOUD_PROJECT environment variable")
    return configuration.Configuration()


@pytest.mark.integration
def test_url(config_obj):
    assert config_obj.url is not None


@pytest.mark.integration
def test_mail(config_obj):
    assert len(config_obj.mail) > 0


@pytest.mark.integration
def test_smtp(config_obj):
    assert config_obj.smtp_server is not None
    assert config_obj.smtp_user is not None
    assert config_obj.smtp_pwd is not None


@pytest.mark.integration
def test_protocol(config_obj):
    assert "tcp" in config_obj.protocol or "udp" in config_obj.protocol


@pytest.mark.integration
def test_access_key(config_obj):
    assert len(config_obj.access_key) >= 16


@pytest.mark.integration
def test_concurrency_number(config_obj):
    assert config_obj.concurrency_number > 0
