 # Code based on and adapted from https://www.codebyamir.com/blog/automated-ebs-snapshots-using-aws-lambda-cloudwatch
 # Backup all specified volumes in a specified region
import boto3
import datetime
import os
import logging
def lambda_handler(event, context):
    logger = logging.getLogger()
    #set log level to INFO
    logger.setLevel(20)
    try:
        ec2 = boto3.client('ec2')
        aws_region =os.environ['aws_region']

        # Connect to region
        ec2 = boto3.client('ec2', region_name=aws_region)

        #Get volume IDs
        input_volume_ids = os.environ['volume_ids']
        volume_ids = input_volume_ids.split(',')

        # Get all in-use volumes in all regions
        result = ec2.describe_volumes( Filters=[{'Name': 'volume-id', 'Values':volume_ids}])

        for volume in result['Volumes']:
            logger.info ("Backing up %s in %s" % (volume['VolumeId'], volume['AvailabilityZone']))
            # Create snapshot
            result = ec2.create_snapshot(VolumeId=volume['VolumeId'],Description='Created by Lambda backup function ebs-snapshots')

            # Get snapshot resource
            ec2resource = boto3.resource('ec2', region_name=aws_region)
            snapshot = ec2resource.Snapshot(result['SnapshotId'])

            volumename      = 'N/A'
            project         = 'N/A'
            environment     = 'N/A'
            timestamp       = snapshot.start_time.strftime("%Y%m%d%H%M")
            created_by      = 'LambdaEbsSnapshot'

            # Retrive tags from volume
            if 'Tags' in volume:
                for tags in volume['Tags']:
                    if tags["Key"] == 'Name':
                        volumename = tags["Value"]
                    if tags["Key"] == 'Project':
                        project = tags["Value"]
                    if tags["Key"] == 'Environment':
                        environment = tags["Value"]

            snapshottags = [{
                   "Key" : "Name",
                   "Value" : volumename + "/backup-" + timestamp
                },
                {
                   "Key" : "Volume_name",
                   "Value" : volumename
                },
                {
                   "Key" : "Project",
                   "Value" : project
                },
                {
                   "Key" : "Environment",
                   "Value" : environment
                },
                {
                   "Key" : "Created_at",
                   "Value" : timestamp
                },
                {
                    "Key" : "Created_by",
                   "Value" : created_by
                }
                ]

            # Add tags to snapshot
            snapshot.create_tags(Tags=snapshottags)
    except Exception as e:
        logger.error('Snapshot backup Lambda failed.')
        print(type(e))
        raise e
