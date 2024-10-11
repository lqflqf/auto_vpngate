import pytest
import configuration


@pytest.fixture
def config_obj():
    return configuration.Configuration()


def test_url(config_obj):
    assert config_obj.url is not None


def test_mail(config_obj):
    assert len(config_obj.mail) > 0


def test_smtp(config_obj):
    assert (config_obj.smtp_server is not None and config_obj.smtp_user is not None and config_obj.smtp_pwd is not None)


def test_protocol(config_obj):
    assert ("tcp" in config_obj.protocol or "udp" in config_obj.protocol)


def test_access_key(config_obj):
    assert len(config_obj.access_key) >= 16


def test_concurrency_number(config_obj):
    assert config_obj.concurrency_number > 0
