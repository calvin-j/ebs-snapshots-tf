output "arn" {
  value = "${aws_lambda_function.main.arn}"
}

output "function_name" {
  value = "${aws_lambda_function.main.function_name}"
}

output "qualified_arn" {
  value = "${aws_lambda_function.main.qualified_arn}"
}

output "invoke_arn" {
  value = "${aws_lambda_function.main.invoke_arn}"
}

output "version" {
  value = "${aws_lambda_function.main.version}"
}

output "alias_name" {
  value = "${aws_lambda_alias.main.name}"
}

output "role_name" {
  value = "${aws_iam_role.main.name}"
}

output "log_group_name" {
  value = "${aws_cloudwatch_log_group.main.name}"
}
