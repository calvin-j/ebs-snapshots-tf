# Changelog

All notable changes to this module are documented in this file.

## 2026-05-14 — 2026 modernisation

The module was last touched in March 2018 and was written for Terraform
0.10.7 / 0.11. This release brings it forward to a working, supported
2026 toolchain. No resource names or module input variables have been
renamed, so existing state should migrate without recreation; however,
the deprecated-resource swaps below do change resource addresses and
will require `terraform state mv` for in-place upgrades.

### Added
- `versions.tf` pinning `terraform >= 1.9.0`, `aws ~> 5.80`, and
  `archive ~> 2.4`.
- `NOTICE` file with a copyright line for 2018-2026.
- `CHANGELOG.md` (this file).
- `.gitignore` entries for `__pycache__/`, `*.pyc`, and
  `.terraform.lock.hcl`.

### Changed
- Every `.tf` file migrated from Terraform 0.11 to 1.x syntax:
  interpolation wrappers dropped, quoted type names replaced with the
  corresponding type constraints (`string`, `number`, `bool`,
  `list(string)`, `map(string)`), `map(...)` calls replaced with object
  literals, and the nested-interpolation ternary in
  `lambda/lambda_alias.tf` fixed.
- Local Lambda sub-module source set to `./lambda` (TF 1.x requires
  relative paths to start with `./` or `../`).
- Lambda runtime bumped from `python2.7` to `python3.13`.
- README rewritten: compatibility section now lists the real supported
  versions; example config rewritten in 1.x syntax; placeholder account
  ID fixed to a valid 12-digit value; typos corrected.

### Replaced (deprecated → current)
- `aws_s3_bucket_object` → `aws_s3_object` (AWS provider 4.x+).
- `aws_cloudwatch_event_rule.is_enabled` → `state` (AWS provider 5.x+).
- `aws_iam_policy_attachment` → `aws_iam_role_policy_attachment` for
  the Lambda logging policy.
