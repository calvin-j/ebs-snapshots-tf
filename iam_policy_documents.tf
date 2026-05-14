data "aws_iam_policy_document" "create_ebs_snapshot" {
  statement {
    effect = "Allow"
    sid    = "AllowCreateSnapshots"

    actions = [
      "ec2:DescribeVolumes",
      "ec2:DescribeTags",
      "ec2:DescribeSnapshots",
      "ec2:CreateSnapshot",
      "ec2:CreateTags",
    ]

    resources = ["*"]
  }
}

data "aws_iam_policy_document" "delete_ebs_snapshot" {
  statement {
    effect = "Allow"
    sid    = "AllowDescribeSnapshots"

    actions = [
      "ec2:DescribeSnapshots",
    ]

    resources = ["*"]
  }

  statement {
    effect    = "Allow"
    sid       = "AllowDeleteTaggedSnapshots"
    actions   = ["ec2:DeleteSnapshot"]
    resources = ["*"]

    condition {
      test     = "StringEquals"
      variable = "aws:ResourceTag/Created_by"
      values   = ["LambdaEbsSnapshot"]
    }
  }
}
