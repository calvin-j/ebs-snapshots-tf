# Code adapted from https://www.codebyamir.com/blog/automated-ebs-snapshots-using-aws-lambda-cloudwatch
# Backup and tag all specified volumes in a given region.
import logging
import os
from datetime import datetime, timezone

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def validate_volumes(env_volume_ids, returned_volumes):
    if len(env_volume_ids) != len(returned_volumes):
        logger.warning(
            "One or more of your volume IDs are invalid or do not exist in the specified region"
        )
    else:
        logger.info("All Volume IDs are valid")


def build_snapshot_tags(volume, timestamp):
    volumename = "N/A"
    project = "N/A"
    environment = "N/A"

    for tag in volume.get("Tags", []):
        if tag["Key"] == "Name":
            volumename = tag["Value"]
        elif tag["Key"] == "Project":
            project = tag["Value"]
        elif tag["Key"] == "Environment":
            environment = tag["Value"]

    return [
        {"Key": "Name", "Value": f"{volumename}/backup-{timestamp}"},
        {"Key": "Volume_name", "Value": volumename},
        {"Key": "Project", "Value": project},
        {"Key": "Environment", "Value": environment},
        {"Key": "Created_at", "Value": timestamp},
        {"Key": "Created_by", "Value": "LambdaEbsSnapshot"},
    ]


def lambda_handler(event, context):
    try:
        aws_region = os.environ["aws_region"]
        volume_ids = os.environ["volume_ids"].split(",")

        ec2 = boto3.client("ec2", region_name=aws_region)

        # Get all volumes matching the configured IDs
        result = ec2.describe_volumes(
            Filters=[{"Name": "volume-id", "Values": volume_ids}]
        )

        validate_volumes(volume_ids, result["Volumes"])

        for volume in result["Volumes"]:
            logger.info(
                f"Backing up {volume['VolumeId']} in {volume['AvailabilityZone']}"
            )

            # Tag at creation time so a snapshot can never exist without its
            # Created_by tag (otherwise the cleanup Lambda would skip it).
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
            snapshot_tags = build_snapshot_tags(volume, timestamp)

            snapshot = ec2.create_snapshot(
                VolumeId=volume["VolumeId"],
                Description="Created by Lambda backup function ebs-snapshots",
                TagSpecifications=[
                    {"ResourceType": "snapshot", "Tags": snapshot_tags}
                ],
            )
            logger.info(f"Created snapshot {snapshot['SnapshotId']}")
    except Exception:
        logger.exception("Snapshot backup Lambda failed.")
        raise
