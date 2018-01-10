data "aws_iam_policy_document" "create_ebs_snapshot" {
  statement {
    effect = "Allow"
    sid    = "AllowCreateSnapshots"

    actions = [
      "ec2:Describe*",
      "ec2:CreateSnapshot",
      "ec2:CreateTags",
      "ec2:DescribeTags",
      "ec2:ModifySnapshotAttribute",
      "ec2:ResetSnapshotAttribute",
    ]

    resources = ["*"]
  }
}

data "aws_iam_policy_document" "delete_ebs_snapshot" {
  statement {
    effect = "Allow"
    sid    = "AllowDeleteSnapshots"

    actions = [
      "ec2:Describe*",
      "ec2:DeleteSnapshot",
    ]

    resources = ["*"]
  }
}
