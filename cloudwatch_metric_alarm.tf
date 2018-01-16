resource "aws_cloudwatch_metric_alarm" "ebs_snapshot_failure" {
  alarm_name = "${format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    "ebs-snapshot-failure"
  )}"

  alarm_description   = "This metric monitors for EBS snapshot failures."
  namespace           = "${var.cw_alarm_namespace}"
  metric_name         = "FailureCount"
  statistic           = "Sum"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  period              = 60
  evaluation_periods  = 1
  threshold           = 1
  alarm_actions       = ["${var.cw_alarm_failure_actions}"]
  treat_missing_data  = "notBreaching"
}

resource "aws_cloudwatch_metric_alarm" "ebs_snapshot_cleanup_failure" {
  alarm_name = "${format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    "ebs-snapshot-cleanup-failure"
  )}"

  alarm_description   = "This metric monitors for EBS snapshot cleanup failures."
  namespace           = "${var.cleanup_cw_alarm_namespace}"
  metric_name         = "FailureCount"
  statistic           = "Sum"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  period              = 60
  evaluation_periods  = 1
  threshold           = 1
  alarm_actions       = ["${var.cleanup_cw_alarm_failure_actions}"]
  treat_missing_data  = "notBreaching"
}
