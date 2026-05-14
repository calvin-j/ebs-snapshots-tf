plugin "terraform" {
  enabled = true
  preset  = "recommended"
}

plugin "aws" {
  enabled = true
  version = "0.34.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

# python3.13 is a valid Lambda runtime; this pinned ruleset predates it.
rule "aws_lambda_function_invalid_runtime" {
  enabled = false
}
