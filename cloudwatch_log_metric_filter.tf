resource "aws_cloudwatch_log_metric_filter" "ebs_snapshot_failure" {
  name = "${format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    "ebs-snapshot-failure"
  )}"

  pattern        = "${var.log_error_pattern}"
  log_group_name = "${module.lambda_ebs_snapshots.log_group_name}"

  metric_transformation {
    name      = "FailureCount"
    namespace = "${var.cw_alarm_namespace}"
    value     = "1"
  }
}

resource "aws_cloudwatch_log_metric_filter" "ebs_snapshot_cleanup_failure" {
  name = "${format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    "ebs-snapshot-cleanup-failure"
  )}"

  pattern        = "${var.cleanup_log_error_pattern}"
  log_group_name = "${module.lambda_ebs_snapshots_cleanup.log_group_name}"

  metric_transformation {
    name      = "FailureCount"
    namespace = "${var.cleanup_cw_alarm_namespace}"
    value     = "1"
  }
}
