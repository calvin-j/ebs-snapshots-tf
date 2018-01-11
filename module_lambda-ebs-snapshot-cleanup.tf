module "lambda_ebs_snapshots_cleanup" {
  source      = "lambda"
  name        = "ebs-snapshots-cleanup"
  project     = "${var.project}"
  environment = "${var.environment}"
  component   = "${var.component}"

  s3_bucket              = "${var.cleanup_s3_bucket}"
  s3_key                 = "${var.cleanup_s3_key}"
  publish                = "${var.cleanup_publish}"
  memory_size            = "${var.cleanup_memory_size}"
  timeout                = "${var.cleanup_timeout}"
  cwlg_retention_in_days = "${var.cleanup_cwlg_retention}"

  runtime = "python2.7"
  handler = "ebs_cleanup_lambda.lambda_handler"

  principal_service  = "events"
  invoker_source_arn = "${aws_cloudwatch_event_rule.ebs_snapshot_cleanup.arn}"

  env_variables = {
    aws_region              = "${var.aws_region}"
    snapshot_retention_days = "${var.snapshot_retention_days}"
    aws_account_id          = "${data.aws_caller_identity.current.account_id}"
    min_number_to_retain    = "${var.min_snapshots_per_vol}"
  }
}

data "archive_file" "cleanup_lambda" {
  type        = "zip"
  source_file = "${path.module}/functions/ebs_cleanup_lambda.py"
  output_path = "${path.module}/artefacts/cleanup_lambda.zip"
}
