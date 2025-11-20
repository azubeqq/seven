# main.tf
# Основные ресурсы: security group, key pair (optional), EC2 instance.
# Inventory file для Ansible будет записан в ../ansible/inventory.ini через provisioner.

# Security Group: разрешим SSH + нужные сервисные порты
resource "aws_security_group" "app_sg" {
  name        = "${var.instance_name}-sg"
  description = "Allow SSH, Flask, Prometheus, Grafana, Loki + Promtail"

  # SSH
  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Flask
  ingress {
    description = "Flask application"
    from_port   = var.flask_port
    to_port     = var.flask_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Prometheus
  ingress {
    description = "Prometheus metrics & UI"
    from_port   = var.prometheus_port
    to_port     = var.prometheus_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Grafana
  ingress {
    description = "Grafana dashboards"
    from_port   = var.grafana_port
    to_port     = var.grafana_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Alertmanager
  ingress {
    description = "Alertmanager UI"
    from_port   = var.alertmanager_port
    to_port     = var.alertmanager_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
   # Loki
  ingress {
    description = "Loki description"
    from_port   = var.loki_port
    to_port     = var.loki_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Разрешаем весь исходящий трафик
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Optionally create (or import) a key-pair.
# If you already have a key in AWS with the same name, comment this out.
#resource "aws_key_pair" "deployer" {
#  key_name   = var.key_name
#  public_key = file(var.public_key_path)
#}

# EC2 instance
resource "aws_instance" "app_server" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.app_sg.id]

# Увеличиваем размер диска, т.к. будут Docker образы
  root_block_device {
    volume_size = var.volume_size  # GB (дефолт 8GB может быть мало)
    volume_type = var.volume_type  # Современный тип диска
  }

  tags = {
    Name        = var.instance_name
    Environment = "dev"
    ManagedBy   = "terraform"
  }

  # После создания запишем публичный IP в файл inventory для Ansible
  provisioner "local-exec" {
    command = "echo '[aws]' > ../ansible/inventory.ini && echo '${self.public_ip} ansible_user=ec2-user ansible_ssh_private_key_file=~/.ssh/${var.key_name}.pem' >> ../ansible/inventory.ini"
  }
}