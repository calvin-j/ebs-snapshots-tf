resource "aws_lambda_alias" "main" {
  name             = "${var.environment}"
  description      = "Alias for ${aws_lambda_function.main.function_name}"
  function_name    = "${aws_lambda_function.main.arn}"
  function_version = "${var.publish ? "${aws_lambda_function.main.version}" : "$LATEST"}"
}
