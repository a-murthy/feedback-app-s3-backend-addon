variable "hcp_organization" {
  type        = string
  default     = "apoorva-murthy-org"
  description = "Your exact HCP Terraform Organization Name."
}

variable "target_app_name" {
  type        = string
  description = "The unique app_name of the Application this add-on belongs to (e.g., feedback-app)."
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "The target AWS region for deployment."
}

variable "maintenance_mode" {
  type        = string
  default     = "false"
  description = "Operational toggle to trigger an immediate Day 2 app maintenance lockout state."
}

# ==============================================================================
# NATIVE PORTAL AUTOMATION: Declarations required by the Developer Portal Beta
# ==============================================================================
variable "developer_portal_application" {
  type    = any
  default = null
}

variable "developer_portal_add_on_definition" {
  type    = any
  default = null
}

variable "developer_portal_add_on" {
  type    = any
  default = null
}
