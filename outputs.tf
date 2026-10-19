# ==============================================================================
# STANDARD REUSABLE BLUEPRINT OUTPUTS
# ==============================================================================

output "ai_engine_private_endpoint" {
  description = "Authorized Enterprise AI Service connection string link."
  value       = aws_lambda_function_url.ai_endpoint.function_url
}
