# variables.tf
# Переменные Terraform — все значения удобно менять в terraform.tfvars

variable "region" {
  description = "AWS region to deploy"
  type        = string
  default     = "eu-central-1"
}

variable "access_key" {
  description = "AWS access key account to deploy"
  type        = string
  default     = "none"
}

variable "secret_key" {
  description = "AWS secret key account to deploy"
  type        = string
  default     = "none"
}

variable "ami_id" {
  description = "AMI to use for the EC2 instance (Ubuntu/AMIs etc.)"
  type        = string
  default     = "ami-0a5b0d219e493191b" # <- пример, замените на актуальную для вашего региона
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "instance_name" {
  description = "Tag Name for the instance"
  type        = string
  default     = "flask-monitoring-server"
}

variable "volume_size" {
  description = "Volume size for EC2 disk"
  type        = number
  default     = 8
}

variable "volume_type" {
  description = "Volume type for EC2 disk"
  type        = string
  default     = "gp3"
}

# SSH key info (must be provided by you)
variable "key_name" {
  description = "Existing AWS keypair name (must exist in your account)"
  type        = string
}

#variable "public_key_path" {
#  description = "Path to public key file to upload to AWS (used to create key pair if needed)"
#  type        = string
#}

# Ports we will open in Security Group
variable "flask_port" {
  type    = number
  default = 5000
}
variable "prometheus_port" {
  type    = number
  default = 9090
}
variable "grafana_port" {
  type    = number
  default = 3000
}
variable "alertmanager_port" {
  type    = number
  default = 9093
}
variable "loki_port" {
  type    = number
  default = 3100
}
variable "promtail_port" {
  type    = number
  default = 9080
}