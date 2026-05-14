import logging

import boto3
import pytest
from moto import mock_aws

import ebs_snapshot_lambda


REGION = "eu-west-1"


def _create_volume(ec2, tags=None):
    kwargs = {"AvailabilityZone": f"{REGION}a", "Size": 1}
    if tags is not None:
        kwargs["TagSpecifications"] = [{"ResourceType": "volume", "Tags": tags}]
    return ec2.create_volume(**kwargs)["VolumeId"]


def test_validate_volumes_match(caplog):
    result = {"Volumes": [{"VolumeId": "vol-1"}, {"VolumeId": "vol-2"}]}
    with caplog.at_level(logging.INFO):
        ebs_snapshot_lambda.validate_volumes(["vol-1", "vol-2"], result)
    assert "All Volume IDs are valid" in caplog.text
    assert "invalid" not in caplog.text


def test_validate_volumes_mismatch(caplog):
    result = {"Volumes": [{"VolumeId": "vol-1"}]}
    with caplog.at_level(logging.WARNING):
        ebs_snapshot_lambda.validate_volumes(["vol-1", "vol-missing"], result)
    assert "invalid or do not exist" in caplog.text


@mock_aws
def test_lambda_handler_creates_tagged_snapshot(monkeypatch, snapshot_env):
    ec2 = boto3.client("ec2", region_name=REGION)
    vol_id = _create_volume(
        ec2,
        tags=[
            {"Key": "Name", "Value": "data-volume"},
            {"Key": "Project", "Value": "alpha"},
            {"Key": "Environment", "Value": "prod"},
        ],
    )
    monkeypatch.setenv("volume_ids", vol_id)

    ebs_snapshot_lambda.lambda_handler({}, None)

    snapshots = ec2.describe_snapshots(
        Filters=[{"Name": "volume-id", "Values": [vol_id]}]
    )["Snapshots"]
    assert len(snapshots) == 1
    tags = {t["Key"]: t["Value"] for t in snapshots[0]["Tags"]}
    assert tags["Volume_name"] == "data-volume"
    assert tags["Project"] == "alpha"
    assert tags["Environment"] == "prod"
    assert tags["Created_by"] == "LambdaEbsSnapshot"
    assert tags["Name"].startswith("data-volume/backup-")
    assert tags["Name"].split("-")[-1] == tags["Created_at"]


@mock_aws
def test_lambda_handler_defaults_to_NA_when_tags_missing(monkeypatch, snapshot_env):
    ec2 = boto3.client("ec2", region_name=REGION)
    vol_id = _create_volume(ec2)
    monkeypatch.setenv("volume_ids", vol_id)

    ebs_snapshot_lambda.lambda_handler({}, None)

    snapshots = ec2.describe_snapshots(
        Filters=[{"Name": "volume-id", "Values": [vol_id]}]
    )["Snapshots"]
    assert len(snapshots) == 1
    tags = {t["Key"]: t["Value"] for t in snapshots[0]["Tags"]}
    assert tags["Volume_name"] == "N/A"
    assert tags["Project"] == "N/A"
    assert tags["Environment"] == "N/A"
    assert tags["Name"].startswith("N/A/backup-")


def test_lambda_handler_raises_on_missing_env(monkeypatch, caplog):
    monkeypatch.delenv("aws_region", raising=False)
    with caplog.at_level(logging.ERROR):
        with pytest.raises(KeyError):
            ebs_snapshot_lambda.lambda_handler({}, None)
    assert "Snapshot backup Lambda failed" in caplog.text
