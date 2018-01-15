variable "project" {
  type        = "string"
  description = "Name of the project."
}

variable "environment" {
  type        = "string"
  description = "Name of the environment."
}

variable "component" {
  type        = "string"
  description = "Name of the component."
}

variable "default_tags" {
  type        = "map"
  description = "Default tags to apply to resources."
  default     = {}
}

variable "name" {
  type        = "string"
  description = "Name of the Lambda"
}

#ebs snapshot lambda
variable "memory_size" {
  type        = "string"
  description = "Amount of memory in MB your Lambda Function can use at runtime. "
}

variable "publish" {
  type        = "string"
  description = "Whether to publish creation/change as new Lambda Function Version"
}

variable "timeout" {
  type        = "string"
  description = " The amount of time your Lambda Function has to run in seconds. "
}

variable "env_vars" {
  type        = "map"
  description = "Environment variables to create the Lambda function with."
  default     = {}
}

variable "volume_ids" {
  type        = "list"
  description = "Volume ids to backup. These should be added as module outputs"
}

variable "aws_region" {
  type        = "string"
  description = ""
}

variable "s3_bucket" {
  type        = "string"
  description = "S3 bucket that the backup Lambda code is stored in"
}

variable "s3_key" {
  type        = "string"
  description = "S3 key that the backup Lambda code is stored in"
}

variable "cwlg_retention" {
  type        = "string"
  description = "Specifies the number of days you want to retain log events in the specified log group."
}

variable "cw_rule_schedule_expression" {
  type        = "string"
  description = "The scheduling expression. Required, if event_pattern isn't specified. Cron or rate format can be specified"
}

variable "log_error_pattern" {
  type        = "string"
  description = "A valid CloudWatch Logs filter pattern for extracting metric data out of ingested log events."
}

variable "cw_alarm_failure_actions" {
  type        = "list"
  description = "The list of actions to execute when this alarm transitions into an ALARM state from any other state. Each action is specified as an ARN"
}

variable "cw_alarm_namespace" {
  type        = "string"
  description = "The namespace for the associated metric. See docs for the list of namespaces. See docs for supported metrics."
}

variable "cw_rule_enabled" {
  type        = "string"
  description = "Whether the rule should be enabled."
}

variable "cleanup_s3_bucket" {
  type        = "string"
  description = "S3 bucket that the backup cleanup Lambda code is stored in"
}

variable "cleanup_s3_key" {
  type        = "string"
  description = "S3 key that the cleanup Lambda code is stored in"
}

variable "cleanup_publish" {
  type        = "string"
  description = "Whether to publish creation/change as new Lambda Function Version"
}

variable "cleanup_memory_size" {
  type        = "string"
  description = "Amount of memory in MB your Lambda Function can use at runtime."
}

variable "cleanup_timeout" {
  type        = "string"
  description = "The amount of time your Lambda Function has to run in seconds."
}

variable "cleanup_cwlg_retention" {
  type        = "string"
  description = "Specifies the number of days you want to retain log events in the specified log group."
}

variable "snapshot_retention_days" {
  type        = "string"
  description = "How many days snapshots should be retained before being considered for cleanup."
}

variable "min_snapshots_per_vol" {
  type        = "string"
  description = "The minimum number of snapshots per volume that should exist before a snapshot that is older than the retention period is deleted"
}

variable "cleanup_cw_alarm_failure_actions" {
  type        = "list"
  description = "The list of actions to execute when this alarm transitions into an ALARM state from any other state. Each action is specified as an ARN"
}

variable "cleanup_cw_alarm_namespace" {
  type        = "string"
  description = "The namespace for the associated metric. See docs for the list of namespaces. See docs for supported metrics."
}

variable "cleanup_log_error_pattern" {
  type        = "string"
  description = "A valid CloudWatch Logs filter pattern for extracting metric data out of ingested log events."
}

variable "cleanup_cw_rule_schedule_expression" {
  type        = "string"
  description = "The scheduling expression. Required, if event_pattern isn't specified. Cron or rate format can be specified"
}

variable "cleanup_cw_rule_enabled" {
  type        = "string"
  description = "Whether the rule should be enabled."
}
