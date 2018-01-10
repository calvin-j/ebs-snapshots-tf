resource "aws_cloudwatch_event_target" "ebs_snapshot" {
  rule = "${aws_cloudwatch_event_rule.ebs_snapshot.name}"
  arn  = "${module.lambda_ebs_snapshots.arn}"
}

resource "aws_cloudwatch_event_target" "ebs_snapshot_cleanup" {
  rule = "${aws_cloudwatch_event_rule.ebs_snapshot_cleanup.name}"
  arn  = "${module.lambda_ebs_snapshots_cleanup.arn}"
}
