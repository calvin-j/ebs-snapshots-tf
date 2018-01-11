resource "aws_iam_policy" "create_ebs_snapshot" {
  name = "${format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    "create-ebs-snapshot"
  )}"

  description = "Grant EBS snapshot creation permissions to Lambda"
  policy      = "${data.aws_iam_policy_document.create_ebs_snapshot.json}"
}

resource "aws_iam_role_policy_attachment" "create_ebs_snapshot" {
  role       = "${module.lambda_ebs_snapshots.role_name}"
  policy_arn = "${aws_iam_policy.create_ebs_snapshot.arn}"
}

resource "aws_iam_policy" "delete_ebs_snapshot" {
  name = "${format(
    "%s-%s-%s-%s",
    var.project,
    var.environment,
    var.component,
    "delete-ebs-snapshot"
  )}"

  description = "Grant EBS snapshot deletion permissions to Lambda"
  policy      = "${data.aws_iam_policy_document.delete_ebs_snapshot.json}"
}

resource "aws_iam_role_policy_attachment" "delete_ebs_snapshot" {
  role       = "${module.lambda_ebs_snapshots_cleanup.role_name}"
  policy_arn = "${aws_iam_policy.delete_ebs_snapshot.arn}"
}
