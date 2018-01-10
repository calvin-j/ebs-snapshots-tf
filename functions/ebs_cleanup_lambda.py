# Code based on and adapted from https://www.codebyamir.com/blog/automated-ebs-snapshots-using-aws-lambda-cloudwatch
import boto3
import logging
import os
from botocore.exceptions import ClientError
from datetime import datetime,timedelta

def delete_snapshot(snapshot_id, reg):
    logger = logging.getLogger()
    # Set log level to INFO
    logger.setLevel(20)
    logger.info("Deleting snapshot %s " % (snapshot_id))
    try:
        ec2resource = boto3.resource('ec2', region_name=reg)
        snapshot = ec2resource.Snapshot(snapshot_id)
        snapshot.delete()
    except ClientError as e:
        logger.error("Caught exception: %s" % e)
        logger.error("Snapshot Cleanup Lambda failed.")

    return

def lambda_handler(event, context):
    logger = logging.getLogger()
    # Set log level to INFO
    logger.setLevel(20)

    try:
        # Get Environment Variables
        aws_account_id = os.environ['aws_account_id']
        # Define retention period in days
        retention_days = int(os.environ['snapshot_retention_days'])
        N_days_ago_retention_days = int(retention_days)
        aws_region = os.environ['aws_region']
        min_num_snapshots_to_keep = int(os.environ['min_number_to_retain'])

        now = datetime.now()
        # Work out the date N days ago - log as useful
        date_N_days_ago =   now - timedelta(days=N_days_ago_retention_days)
        logger.info("Time N days ago %s" % date_N_days_ago)

        # Create EC2 client
        ec2 = boto3.client('ec2')

        # Connect to region
        ec2 = boto3.client('ec2',region_name=aws_region)

        # Filtering by snapshot timestamp comparison is not supported
        # So we grab all snapshot ids of snapshots that were created using the backup Lambda
        result = ec2.describe_snapshots(OwnerIds=[aws_account_id], Filters=[{'Name': 'tag:Created_by', 'Values': ["LambdaEbsSnapshot"]}])

        for snapshot in result['Snapshots']:
            logger.info ("Checking snapshot %s which was created on %s" % (snapshot['SnapshotId'],snapshot['StartTime']))
            # Remove timezone info from snapshot in order for comparison to work below
            snapshot_time = snapshot['StartTime'].replace(tzinfo=None)

            # Subtract snapshot time from now returns a timedelta
            # Check if the timedelta is greater than retention days
            if (now - snapshot_time) > timedelta(retention_days):
                logger.info("Snapshot is older than configured retention of %d days" % retention_days)
                # Additional check to pull out volume ID then make sure there are at least N retention days of snapshots before deleting
                snapshot_vol_id = snapshot['VolumeId']
                split_snapshot_vol_id = snapshot_vol_id.split(',')
                logger.info ("Volume associated with this snapshot is %s" % split_snapshot_vol_id)
                # Retrive all snapshots for the same volume
                volume_result = ec2.describe_snapshots(Filters=[{'Name': 'volume-id', 'Values':split_snapshot_vol_id}, {'Name': 'tag:Created_by', 'Values': ["LambdaEbsSnapshot"]}])
                retained_snapshots =0
                # Count the number of snapshots associated with this volume
                for volume in volume_result['Snapshots']:
                        retained_snapshots +=1

                if retained_snapshots > min_num_snapshots_to_keep:
                    delete_snapshot(snapshot['SnapshotId'], aws_region)
                else:
                    logger.info ("There are only %s retained snapshots for this volume so we keep this snapshot" % retained_snapshots)

            else:
                logger.info ("Snapshot %s is newer than configured retention of %d days so we keep it" % (snapshot['SnapshotId'],retention_days))

    except Exception as e:
        logger.error("Snapshot Cleanup Lambda failed.")
        print(type(e))
        raise e
