mock_provider "aws" {}
mock_provider "archive" {}

variables {
  project     = "test"
  environment = "ci"
  component   = "ebs"

  snapshot_name = "ebs-snapshots"
  cleanup_name  = "ebs-snapshots-cleanup"

  memory_size = 200
  publish     = true
  timeout     = 60

  snapshot_s3_bucket = "test-snapshots-lambda"
  snapshot_s3_key    = "lambda/ebs_snapshot_lambda.py.zip"

  cwlg_retention = 30
  aws_region     = "eu-west-1"

  volume_ids = ["vol-00000000000000001", "vol-00000000000000002"]

  cw_rule_enabled             = true
  cw_rule_schedule_expression = "cron(00 01 ? * 3-7 *)"

  log_error_pattern        = "\"[ERROR]\" \"Snapshot backup Lambda failed\""
  cw_alarm_failure_actions = ["arn:aws:sns:eu-west-1:123456789012:alert"]
  cw_alarm_namespace       = "test-ci-ebs-ebs-snapshot-lambda"

  snapshot_retention_days = 7
  min_snapshots_per_vol   = 7

  cleanup_cw_rule_enabled = true

  cleanup_memory_size = 200
  cleanup_publish     = true
  cleanup_timeout     = 120

  cleanup_s3_bucket = "test-snapshots-lambda"
  cleanup_s3_key    = "lambda/ebs_cleanup_lambda.py.zip"

  cleanup_cwlg_retention              = 30
  cleanup_cw_rule_schedule_expression = "cron(00 03 ? * 3-7 *)"

  cleanup_log_error_pattern        = "\"[ERROR]\" \"Snapshot Cleanup Lambda failed\""
  cleanup_cw_alarm_failure_actions = ["arn:aws:sns:eu-west-1:123456789012:alert"]
  cleanup_cw_alarm_namespace       = "test-ci-ebs-ebs-snapshot-cleanup-lambda"
}

run "valid_plan" {
  command = plan

  assert {
    condition     = module.lambda_ebs_snapshots.function_name == "test-ci-ebs-ebs-snapshots"
    error_message = "Snapshot Lambda function name not composed correctly"
  }

  assert {
    condition     = module.lambda_ebs_snapshots_cleanup.function_name == "test-ci-ebs-ebs-snapshots-cleanup"
    error_message = "Cleanup Lambda function name not composed correctly"
  }

  assert {
    condition     = aws_cloudwatch_event_rule.ebs_snapshot.schedule_expression == "cron(00 01 ? * 3-7 *)"
    error_message = "Snapshot event rule schedule not wired through"
  }

  assert {
    condition     = aws_cloudwatch_event_rule.ebs_snapshot_cleanup.schedule_expression == "cron(00 03 ? * 3-7 *)"
    error_message = "Cleanup event rule schedule not wired through"
  }

  assert {
    condition     = aws_cloudwatch_event_rule.ebs_snapshot.state == "ENABLED"
    error_message = "Snapshot event rule should be enabled"
  }
}

run "rule_disabled_when_flag_false" {
  command = plan

  variables {
    cw_rule_enabled         = false
    cleanup_cw_rule_enabled = false
  }

  assert {
    condition     = aws_cloudwatch_event_rule.ebs_snapshot.state == "DISABLED"
    error_message = "Snapshot event rule should be disabled when cw_rule_enabled = false"
  }

  assert {
    condition     = aws_cloudwatch_event_rule.ebs_snapshot_cleanup.state == "DISABLED"
    error_message = "Cleanup event rule should be disabled when cleanup_cw_rule_enabled = false"
  }
}
