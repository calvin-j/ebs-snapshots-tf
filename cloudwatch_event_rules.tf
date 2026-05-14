resource "aws_cloudwatch_event_rule" "ebs_snapshot" {
  name = format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    "ebs-snapshot",
  )

  description         = "Snapshot EBS volumes"
  schedule_expression = var.cw_rule_schedule_expression
  state               = var.cw_rule_enabled ? "ENABLED" : "DISABLED"
}

resource "aws_cloudwatch_event_rule" "ebs_snapshot_cleanup" {
  name = format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    "ebs-snapshot-cleanup",
  )

  description         = "Cleanup EBS volume snapshots"
  schedule_expression = var.cleanup_cw_rule_schedule_expression
  state               = var.cleanup_cw_rule_enabled ? "ENABLED" : "DISABLED"
}
