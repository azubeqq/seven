# ========================================
# TERRAFORM PROVIDERS CONFIGURATION
# ========================================

# --- Required Terraform Version ---
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }

  # Опционально: backend для хранения state в S3 (для команды)
  # backend "s3" {
  #   bucket = "your-terraform-state-bucket"
  #   key    = "flask-monitoring/terraform.tfstate"
  #   region = "eu-central-1"
  #   encrypt = true
  #   dynamodb_table = "terraform-state-lock"
  # }
}

# --- AWS Provider ---
provider "aws" {
  region     = var.region
  
  # ЛУЧШИЙ СПОСОБ: использовать AWS CLI профили или env переменные
  # export AWS_PROFILE=your_profile
  # или
  # export AWS_ACCESS_KEY_ID=xxx
  # export AWS_SECRET_ACCESS_KEY=yyy
  
  # Если всё же используешь переменные (не рекомендуется):
  access_key = var.access_key != "" ? var.access_key : null
  secret_key = var.secret_key != "" ? var.secret_key : null

  # Теги по умолчанию для всех ресурсов
  default_tags {
    tags = {
      Project   = "Flask-Monitoring"
      ManagedBy = "Terraform"
    }
  }
}