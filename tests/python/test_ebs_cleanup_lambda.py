import logging
from datetime import datetime, timedelta, timezone

import boto3
import pytest
from botocore.exceptions import ClientError

import ebs_cleanup_lambda


REGION = "eu-west-1"
ACCOUNT_ID = "123456789012"


def _make_volume_and_snapshots(ec2, count):
    vol_id = ec2.create_volume(AvailabilityZone=f"{REGION}a", Size=1)["VolumeId"]
    snap_ids = []
    for _ in range(count):
        snap_id = ec2.create_snapshot(VolumeId=vol_id, Description="test")["SnapshotId"]
        ec2.create_tags(
            Resources=[snap_id],
            Tags=[{"Key": "Created_by", "Value": "LambdaEbsSnapshot"}],
        )
        snap_ids.append(snap_id)
    return vol_id, snap_ids


def _shift_now_by(monkeypatch, days):
    real_datetime = ebs_cleanup_lambda.datetime

    class ShiftedDatetime(real_datetime):
        @classmethod
        def now(cls, tz=None):
            return real_datetime.now(tz) + timedelta(days=days)

    monkeypatch.setattr(ebs_cleanup_lambda, "datetime", ShiftedDatetime)


def test_sort_snapshots_orders_oldest_first():
    now = datetime.now(tz=timezone.utc)
    result = {
        "Snapshots": [
            {"SnapshotId": "snap-new", "VolumeId": "vol-1", "StartTime": now},
            {"SnapshotId": "snap-old", "VolumeId": "vol-1", "StartTime": now - timedelta(days=10)},
            {"SnapshotId": "snap-mid", "VolumeId": "vol-1", "StartTime": now - timedelta(days=5)},
        ]
    }
    ordered = ebs_cleanup_lambda.sort_snapshots(result)
    assert [s["snap_id"] for s in ordered] == ["snap-old", "snap-mid", "snap-new"]
    assert all(s["date"].tzinfo is None for s in ordered)


def test_delete_snapshot_invokes_delete():
    ec2 = boto3.client("ec2", region_name=REGION)
    _, snap_ids = _make_volume_and_snapshots(ec2, count=1)

    ebs_cleanup_lambda.delete_snapshot(snap_ids[0], REGION)

    remaining = ec2.describe_snapshots(SnapshotIds=[], OwnerIds=[ACCOUNT_ID])["Snapshots"]
    assert all(s["SnapshotId"] != snap_ids[0] for s in remaining)


def test_delete_snapshot_reraises_client_error(caplog):
    # The handler logs the failure and re-raises so the outer
    # lambda_handler exits non-zero (real-world: CloudWatch alarm fires).
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ClientError):
            ebs_cleanup_lambda.delete_snapshot("snap-00000000000000000", REGION)
    assert "Caught exception" in caplog.text


def test_handler_deletes_down_to_below_min_retain(cleanup_env, monkeypatch):
    # min_number_to_retain=2, 4 old snapshots: handler deletes while
    # count >= 2, stopping when count drops below 2. End state: 1 snapshot.
    ec2 = boto3.client("ec2", region_name=REGION)
    _, snap_ids = _make_volume_and_snapshots(ec2, count=4)

    _shift_now_by(monkeypatch, days=30)
    ebs_cleanup_lambda.lambda_handler({}, None)

    remaining = ec2.describe_snapshots(
        OwnerIds=[ACCOUNT_ID],
        Filters=[{"Name": "tag:Created_by", "Values": ["LambdaEbsSnapshot"]}],
    )["Snapshots"]
    assert len(remaining) == 1
    remaining_ids = {s["SnapshotId"] for s in remaining}
    assert remaining_ids.issubset(set(snap_ids))


def test_handler_stops_deleting_once_below_min_retain(cleanup_env, monkeypatch):
    # 2 old snapshots, min=2: delete 1 (count=2 >= 2), skip the next
    # (count=1 < 2). Exactly one snapshot remains.
    ec2 = boto3.client("ec2", region_name=REGION)
    _, snap_ids = _make_volume_and_snapshots(ec2, count=2)

    _shift_now_by(monkeypatch, days=30)
    ebs_cleanup_lambda.lambda_handler({}, None)

    remaining = ec2.describe_snapshots(
        OwnerIds=[ACCOUNT_ID],
        Filters=[{"Name": "tag:Created_by", "Values": ["LambdaEbsSnapshot"]}],
    )["Snapshots"]
    assert len(remaining) == 1
    assert {s["SnapshotId"] for s in remaining}.issubset(set(snap_ids))


def test_handler_keeps_recent_snapshots(cleanup_env):
    ec2 = boto3.client("ec2", region_name=REGION)
    _, snap_ids = _make_volume_and_snapshots(ec2, count=4)

    # No time shift - snapshots are fresh, well within retention window
    ebs_cleanup_lambda.lambda_handler({}, None)

    remaining = ec2.describe_snapshots(
        OwnerIds=[ACCOUNT_ID],
        Filters=[{"Name": "tag:Created_by", "Values": ["LambdaEbsSnapshot"]}],
    )["Snapshots"]
    assert {s["SnapshotId"] for s in remaining} == set(snap_ids)


def test_handler_raises_on_missing_env(monkeypatch, caplog):
    monkeypatch.delenv("aws_account_id", raising=False)
    with caplog.at_level(logging.ERROR):
        with pytest.raises(KeyError):
            ebs_cleanup_lambda.lambda_handler({}, None)
    assert "Snapshot Cleanup Lambda failed" in caplog.text
