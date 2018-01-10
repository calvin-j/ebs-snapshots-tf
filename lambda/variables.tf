variable "project" {
  type        = "string"
  description = "The name of the project."
}

variable "environment" {
  type        = "string"
  description = "The name of the environment."
}

variable "component" {
  type        = "string"
  description = "The name of the component."
}

variable "module" {
  type        = "string"
  description = "The module name."
  default     = "lambda"
}

variable "name" {
  type        = "string"
  description = "Name of the Lambda."
}

variable "s3_bucket" {
  type        = "string"
  description = "The S3 bucket location containing the function's deployment package. "
}

variable "s3_key" {
  type        = "string"
  description = "The S3 key of an object containing the function's deployment package. "
}

variable "runtime" {
  type        = "string"
  description = "The runtime environment for the Lambda function you are uploading"
}

variable "handler" {
  type        = "string"
  description = "The function entrypoint in your code."
}

variable "memory_size" {
  type        = "string"
  description = "Amount of memory in MB your Lambda Function can use at runtime. "
}

variable "timeout" {
  type        = "string"
  description = "The amount of time your Lambda Function has to run in seconds."
}

variable "publish" {
  type        = "string"
  description = "Whether to publish creation/change as new Lambda Function Version"
}

variable "env_variables" {
  type        = "map"
  description = "Map of environment to pass to Lambda"
  default     = {}
}

variable "principal_service" {
  type        = "string"
  description = "A service name allowed to invoke lambda. Accepted values: apigateway, events"
  default     = ""
}

variable "invoker_source_arn" {
  type        = "string"
  description = "The arn of the Principal Service"
  default     = ""
}

variable "cwlg_retention_in_days" {
  type        = "string"
  description = ""
}

variable "default_tags" {
  type        = "map"
  description = ""
  default     = {}
}
