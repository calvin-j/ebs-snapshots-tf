resource "aws_s3_bucket" "lambda-functions" {
  bucket = "${format(
    "%s.%s.%s.%s",
    var.project,
    var.environment,
    var.component,
    "artefacts",
  )}"

  versioning {
    enabled = false
  }

  force_destroy = false

  tags = "${merge(
    var.default_tags,
    map(
      "Name", format(
        "%s-%s-%s/%s",
        var.project,
        var.environment,
        var.component,
        "artefacts",
      )
    )
  )}"
}
