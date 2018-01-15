resource "aws_iam_role" "main" {
  name = "${format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    var.name
  )}"

  assume_role_policy = "${data.aws_iam_policy_document.assumerole.json}"
}
