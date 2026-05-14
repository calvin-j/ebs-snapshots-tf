import os

import pytest


@pytest.fixture(autouse=True)
def aws_credentials(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-west-1")


@pytest.fixture
def snapshot_env(monkeypatch):
    monkeypatch.setenv("aws_region", "eu-west-1")
    monkeypatch.setenv("volume_ids", "")


@pytest.fixture
def cleanup_env(monkeypatch):
    monkeypatch.setenv("aws_account_id", "123456789012")
    monkeypatch.setenv("aws_region", "eu-west-1")
    monkeypatch.setenv("snapshot_retention_days", "7")
    monkeypatch.setenv("min_number_to_retain", "2")
