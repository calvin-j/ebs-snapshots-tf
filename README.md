# ebs-snapshots-tf
Terraform Module for Automated EBS Volume Backups


## Info 

This module includes the necessary Terraform code to configure and manage the required resources to preform automated scheduled snapshotting of EBS volume. 

Automated cleanup of old snapshots created by the backup Lambda according to a defined retention policy is also handled by the module. Both Lambda fucntions included are triggered by scheduled CloudWatch event rules.

A CloudWatch metric filter and an alarm to alert on backup failure are also created and managed. This publishes to a specified SNS topic, of which you will need to subscribe yourself to to receive alerts. 

A requisite Lambda Terraform module, written by [sebolabs](https://github.com/sebolabs) has been included as a nested submodule.

Snapshots are tagged and named according to the tags and name on the source volume. 

## Usage

### Example Config

```
module "ebs-snapshots" {
  source = "github.com/calvin-j/ebs-snapshots-tf.git"

  name        = "ebs-snapshots"
  project     = "${var.project}"
  environment = "${var.environment}"
  component   = "${var.component}"

  cw_rule_enabled = true

  memory_size = 200
  publish     = true
  timeout     = 60

  s3_bucket      = "snapshotslambda"
  s3_key         = "ebs_snapshot_lambda.py.zip"
  cwlg_retention = 30
  aws_region     = "${var.aws_region}"

  volume_ids = ["vol-xxxxxxx", "vol-yyyyyyyy"]

  cw_rule_schedule_expression = "cron(00 01 ? * 3-7 *)"

  log_error_pattern        = "\"[ERROR]\" \"Snapshot backup Lambda failed\""
  cw_alarm_failure_actions = ["arn:aws:sns:eu-west-1:059799936681:notify-admins"]

  cw_alarm_namespace = "${format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    "ebs-snapshot-lambda"
  )}"

  snapshot_retention_days = 7
  min_snapshots_per_vol   = 7

  cleanup_cw_rule_enabled = true

  cleanup_memory_size = 200
  cleanup_publish     = true
  cleanup_timeout     = 120

  cleanup_s3_bucket      = "snapshotslambda"
  cleanup_s3_key         = "ebs_cleanup_lambda.py.zip"
  cleanup_cwlg_retention = 30

  cleanup_cw_rule_schedule_expression = "cron(00 03 ? * 3-7 *)"

  cleanup_log_error_pattern        = "\"[ERROR]\" \"Snapshot Cleanup Lambda failed\""
  cleanup_cw_alarm_failure_actions = ["arn:aws:sns:eu-west-1:12345678900:notify-admins"]

  cleanup_cw_alarm_namespace = "${format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    "ebs-snapshot-cleanup-lambda"
  )}"
}


```
There are two parameters min_num_of_snapshots_to_retain,  min_retention_days. There are self-explanatory however it is worth noting that the minimum number of snapshots to retain will always take precedence, e.g. if retention days is 2 and minimum number to retain is 4 then snapshots will be effectively be retained for 4 days (assuming no previous older snapshots exist & the backup runs once a day). 

N.B. it is not recommended to reduce the timeout value by less than 60 seconds if you require more than a couple of volumes to be backed up as there is a likelihood that the function will timeout without completing. 


You will need to create and specify a S3 bucket for the Lambda artefacts to be stored in. They will automatically be uploaded as bucket objects, stored acording to the s3_key values you set.

You will need to create an SNS topic and subscribe yourself to it if you wish to receive alerts on the failure of any specific functions. and include its arn as a key in *cw_alarm_failure_actions* and *cleanup_cw_alarm_failure_actions*.

### Terraform Compatibility
Tested with 0.10.7
