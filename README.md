# 🤖 AWS ECS Feedback App S3 Backend Add-On Module

An enterprise-grade, fully compliant **Day 1 Add-On Infrastructure Module** built for HCP Terraform No-Code Provisioning workflows. This module seamlessly attaches native, natural language processing (NLP) capabilities and an immutable S3 storage archive layer directly to an existing running application stack.

## 🚀 Architectural Overview
This module provisions:
1. **AWS Lambda Compute**: Private execution logic executing within the primary application's path, running sentiment classifications securely via Amazon Comprehend.
2. **Amazon S3 Storage Archive**: An isolated, secure bucket with strict public access blocks to store structural JSON logs of incoming traffic payloads automatically.

All actions route through standard AWS SDK channels, utilizing pre-existing administrative execution tokens (`LabRole`) to satisfy restricted sandbox boundary configurations.

## 💻 Deployment Workflow (HCP Terraform UI)
This module is optimized entirely for **No-Code Portal Interface Deployment**. Do not execute local terminal `terraform apply` actions.

1. **Publish to Registry**: Push this repository to your connected VCS provider. HCP Terraform will automatically index it as an available No-Code Add-On module.
2. **UI Orchestration**: Navigate to the HCP Terraform Developer Portal UI. Select this Add-On from your catalog.
3. **Automatic Binding**: The interface will prompt you for variables or discover the core application workspace configuration natively.
4. **Execution**: Trigger the workspace run directly through the HCP Terraform UI dashboard.

## 🛠 Day 2 Operations (Actions Engine)
This module includes a UI-triggerable emergency management hook. Changing the `maintenance_mode` operational toggle from `false` to `true` inside the HCP Terraform variables interface forces an immediate out-of-band lockdown event on the target compute stack without altering application source code.
