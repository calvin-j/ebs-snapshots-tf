resource "aws_lambda_function" "main" {
  function_name = format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    var.name,
  )

  description = "${upper(var.name)} lambda function"

  s3_bucket        = var.s3_bucket
  s3_key           = var.s3_key
  source_code_hash = var.source_code_hash

  runtime     = var.runtime
  handler     = var.handler
  memory_size = var.memory_size
  timeout     = var.timeout
  publish     = var.publish

  role = aws_iam_role.main.arn

  environment {
    variables = var.env_variables
  }

  tags = merge(
    var.default_tags,
    {
      Name = format(
        "%s-%s-%s-%s",
        var.project,
        var.environment,
        var.component,
        var.name,
      )
      Module = var.module
    },
  )
}
