# Code adapted from https://www.codebyamir.com/blog/automated-ebs-snapshots-using-aws-lambda-cloudwatch
# Delete all snapshots older than the specified retention period providing
# there are at least N retained snapshots for the source volume.
import logging
import os
from datetime import datetime, timedelta, timezone

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def sort_snapshots(snapshots):
    # Sort ascending by StartTime so the oldest snapshots are evaluated first.
    return sorted(
        (
            {
                "date": snap["StartTime"],
                "snap_id": snap["SnapshotId"],
                "vol_id": snap["VolumeId"],
            }
            for snap in snapshots
        ),
        key=lambda k: k["date"],
    )


def delete_snapshot(ec2_resource, snapshot_id):
    logger.info(f"Deleting snapshot {snapshot_id}")
    try:
        ec2_resource.Snapshot(snapshot_id).delete()
        return True
    except ClientError as e:
        logger.error(f"Caught exception deleting {snapshot_id}: {e}")
        logger.error("Snapshot Cleanup Lambda failed.")
        return False


def lambda_handler(event, context):
    try:
        aws_account_id = os.environ["aws_account_id"]
        retention_days = int(os.environ["snapshot_retention_days"])
        aws_region = os.environ["aws_region"]
        min_num_snapshots_to_keep = int(os.environ["min_number_to_retain"])

        now = datetime.now(timezone.utc)
        retention = timedelta(days=retention_days)
        logger.info(f"Cutoff for deletion is {now - retention} (retention {retention_days} days)")

        ec2 = boto3.client("ec2", region_name=aws_region)
        ec2_resource = boto3.resource("ec2", region_name=aws_region)

        # Snapshot timestamp comparison isn't supported as a filter, so we
        # grab every snapshot created by the backup Lambda and evaluate them.
        result = ec2.describe_snapshots(
            OwnerIds=[aws_account_id],
            Filters=[{"Name": "tag:Created_by", "Values": ["LambdaEbsSnapshot"]}],
        )

        # Per-volume counts built once from the initial result and decremented
        # as we delete. This avoids an extra describe_snapshots call per
        # snapshot, which can trip EC2 API throttling at scale.
        snapshots_per_volume = {}
        for snap in result["Snapshots"]:
            vol_id = snap["VolumeId"]
            snapshots_per_volume[vol_id] = snapshots_per_volume.get(vol_id, 0) + 1

        for snapshot in sort_snapshots(result["Snapshots"]):
            snap_id = snapshot["snap_id"]
            vol_id = snapshot["vol_id"]
            logger.info(f"Checking snapshot {snap_id} which was created on {snapshot['date']}")

            if (now - snapshot["date"]) <= retention:
                logger.info(
                    f"Snapshot {snap_id} is newer than configured retention of {retention_days} days so we keep it"
                )
                continue

            logger.info(f"Snapshot is older than configured retention of {retention_days} days")
            logger.info(f"Volume associated with this snapshot is {vol_id}")

            retained_snapshots = snapshots_per_volume.get(vol_id, 0)
            if retained_snapshots > min_num_snapshots_to_keep:
                if delete_snapshot(ec2_resource, snap_id):
                    snapshots_per_volume[vol_id] = retained_snapshots - 1
            else:
                logger.info(
                    f"There are only {retained_snapshots} retained snapshots for this volume so we keep this snapshot"
                )

    except Exception:
        logger.exception("Snapshot Cleanup Lambda failed.")
        raise
