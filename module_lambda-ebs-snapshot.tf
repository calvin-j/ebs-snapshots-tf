module "lambda_ebs_snapshots" {
  source      = "lambda"
  name        = "${var.name}"
  project     = "${var.project}"
  environment = "${var.environment}"
  component   = "${var.component}"

  s3_bucket              = "${var.s3_bucket}"
  s3_key                 = "${var.s3_key}"
  publish                = "${var.publish}"
  memory_size            = "${var.memory_size}"
  timeout                = "${var.timeout}"
  cwlg_retention_in_days = "${var.cwlg_retention}"

  runtime = "python2.7"
  handler = "ebs_snapshot_lambda.lambda_handler"

  principal_service  = "events"
  invoker_source_arn = "${aws_cloudwatch_event_rule.ebs_snapshot.arn}"

  env_variables = {
    aws_region = "${var.aws_region}"
    volume_ids = "${join(",", var.volume_ids)}"
  }
}

data "archive_file" "snapshot_lambda" {
  type        = "zip"
  source_file = "${path.module}/functions/ebs_snapshot_lambda.py"
  output_path = "${path.module}/artefacts/snapshot_lambda.zip"
}
