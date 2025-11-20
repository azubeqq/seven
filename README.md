🚀 Flask Monitoring Stack на AWS
Учебный DevOps проект: автоматизированное развертывание Flask приложения с полным мониторингом стеком на AWS EC2.
📋 Что внутри?

Infrastructure as Code: Terraform для создания AWS инфраструктуры
Configuration Management: Ansible для автоматизации установки и настройки
Application: Flask приложение с PostgreSQL
Monitoring: Prometheus + Grafana + Alertmanager
Exporters: Node Exporter, cAdvisor, Postgres Exporter

🏗️ Архитектура
┌────────────────────────────────────────────────────┐
│                    AWS EC2 Instance                │
│                                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │         Docker Compose Network               │  │
│  │                                              │  │
│  │  ┌──────────┐  ┌──────────────┐              │  │
│  │  │  Flask   │──│ PostgreSQL   │              │  │
│  │  │   :5000  │  │    :5432     │              │  │
│  │  └──────────┘  └──────────────┘              │  │
│  │       │              │                       │  │
│  │       └──────┬───────┘                       │  │
│  │              ▼                               │  │
│  │       ┌──────────────┐                       │  │
│  │       │ Prometheus   │◄──┐                   │  │
│  │       │    :9090     │   │                   │  │
│  │       └──────────────┘   │                   │  │
│  │              │           │                   │  │
│  │              ▼           │                   │  │
│  │       ┌──────────────┐   │                   │  │
│  │       │   Grafana    │   │                   │  │
│  │       │    :3000     │   │                   │  │
│  │       └──────────────┘   │                   │  │
│  │                          │                   │  │
│  │  Exporters: ─────────────┘                   │  │
│  │    • Node Exporter    :9100                  │  │
│  │    • cAdvisor        :8080                   │  │
│  │    • Postgres Exp.   :9187                   │  │
│  │                                              │  │
│  │       ┌──────────────┐                       │  │
│  │       │ Alertmanager │                       │  │
│  │       │    :9093     │                       │  │
│  │       └──────────────┘                       │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
🚦 Предварительные требования
Локальная машина:

Terraform >= 1.0
Ansible >= 2.9
AWS CLI (опционально)

AWS:

AWS аккаунт
IAM пользователь с правами на EC2, VPC, Security Groups
Созданный SSH ключ в AWS

📦 Быстрый старт
1. Клонировать репозиторий
bashgit clone <your-repo>
cd flask-monitoring-aws
2. Настроить Terraform
Создай файл terraform/terraform.tfvars:
hcl# AWS креденшалы (или используй AWS CLI профиль)
access_key = "your_access_key"
secret_key = "your_secret_key"

# Регион
region = "eu-central-1"

# SSH ключ (должен существовать в AWS!)
key_name = "your-key-name"

# AMI (проверь актуальность для своего региона)
ami_id = "ami-0a5b0d219e493191b"  # Amazon Linux 2023 eu-central-1

# Тип инстанса
instance_type = "t3.micro"
3. Развернуть инфраструктуру
bashcd terraform
terraform init
terraform plan
terraform apply
После успешного apply запиши публичный IP:
bashterraform output public_ip
4. Установить Ansible зависимости
bashcd ../ansible
ansible-galaxy collection install -r requirements.yml
5. Проверить connectivity
bash# Проверь что SSH доступен
ansible aws -m ping

# Если ошибка, подожди ~30 секунд пока инстанс полностью загрузится
6. Запустить Ansible playbook
bashansible-playbook playbooks/deploy_app.yml

# С детальным выводом:
ansible-playbook playbooks/deploy_app.yml -v
7. Проверить результат
После успешного деплоя открой в браузере:

Flask App: http://<PUBLIC_IP>:5000
Prometheus: http://<PUBLIC_IP>:9090
Grafana: http://<PUBLIC_IP>:3000 (admin/admin)
Alertmanager: http://<PUBLIC_IP>:9093

🎯 Что мониторится?
Системные метрики (Node Exporter):

CPU usage
Memory usage
Disk space
Network I/O
Load average

Метрики контейнеров (cAdvisor):

Container CPU/Memory usage
Container network I/O
Container filesystem usage
Container restart count

Метрики приложения (Flask):

HTTP request duration
Request count by endpoint
Error rates (4xx, 5xx)
Active connections

Метрики БД (Postgres Exporter):

Database connections
Transaction rate
Query performance
Database size

🚨 Настроенные алерты
Critical:

✅ Service Down (контейнер недоступен)
✅ Database connection failed
✅ High error rate (5xx)
✅ Critical CPU/Memory usage (>95%)
✅ Critical disk space (<10%)

Warning:

⚠️ High CPU/Memory usage (>80%)
⚠️ Slow Flask response time (>2s)
⚠️ Container high resource usage
⚠️ Low disk space (<20%)

🔧 Настройка алертинга
Email (Gmail):

Создай App Password: https://myaccount.google.com/apppasswords
Раскомментируй секцию в ansible/group_vars/all.yml:

yamlgmail_app_password: "your_app_password"

Зашифруй через ansible-vault:

bashansible-vault encrypt_string 'your_password' --name 'gmail_app_password'

Обнови roles/app/templates/alertmanager.yml.j2 (используй закомментированную секцию)
Запусти playbook повторно

Telegram:

Создай бота через @BotFather
Получи chat_id через @userinfobot
Добавь в group_vars/all.yml:

yamltelegram_bot_token: "your_bot_token"
telegram_chat_id: your_chat_id

Обнови alertmanager.yml.j2
Запусти playbook

📊 Grafana Dashboards
Рекомендуемые дашборды для импорта:

Node Exporter Full (ID: 1860)

Системные метрики хоста


Docker and System Monitoring (ID: 893)

Метрики контейнеров


PostgreSQL Database (ID: 9628)

Метрики базы данных



Импорт: Grafana → Dashboards → Import → Enter ID
🛠️ Полезные команды
SSH подключение:
bashssh -i ~/.ssh/your-key.pem ec2-user@<PUBLIC_IP>
Проверка контейнеров:
bashdocker ps
docker-compose ps
docker logs <container_name>
Перезапуск стека:
bashcd /home/ec2-user/app
docker-compose restart
Проверка метрик вручную:
bashcurl http://localhost:9100/metrics  # Node Exporter
curl http://localhost:8080/metrics  # cAdvisor
curl http://localhost:5000/metrics  # Flask
Пересборка только приложения:
bashdocker-compose up -d --build web
🧹 Очистка ресурсов
bash# Остановить и удалить все контейнеры (на EC2):
cd /home/ec2-user/app
docker-compose down -v

# Удалить AWS инфраструктуру:
cd terraform
terraform destroy
⚠️ ВАЖНО: terraform destroy удалит все ресурсы и данные безвозвратно!
🔒 Security Best Practices
⚠️ Текущие уязвимости (для учебного проекта):

Security Group открыт для 0.0.0.0/0
Пароли в открытом виде в all.yml
Default креденшалы для Grafana
Нет SSL/TLS

🛡️ Для production:

Ограничь Security Group:

hcl   cidr_blocks = ["YOUR_IP/32"]  # только твой IP

Используй Ansible Vault для паролей:

bash   ansible-vault encrypt group_vars/all.yml

Настрой HTTPS (через Nginx reverse proxy + Let's Encrypt)
Используй AWS Secrets Manager для креденшалов
Регулярно обновляй образы Docker

📁 Структура проекта
.
├── ansible/
│   ├── ansible.cfg              # Конфигурация Ansible
│   ├── inventory.ini            # Генерируется Terraform
│   ├── requirements.yml         # Ansible коллекции
│   ├── group_vars/
│   │   └── all.yml             # Глобальные переменные
│   ├── playbooks/
│   │   └── deploy_app.yml      # Основной playbook
│   └── roles/
│       ├── docker/             # Установка Docker
│       │   └── tasks/
│       │       └── main.yml
│       └── app/                # Деплой приложения
│           ├── files/
│           │   └── app/        # Flask код
│           ├── handlers/
│           │   └── main.yml
│           ├── tasks/
│           │   └── main.yml
│           └── templates/      # Jinja2 шаблоны
│               ├── docker-compose.yml.j2
│               ├── prometheus.yml.j2
│               ├── alertmanager.yml.j2
│               └── alert_rules.yml.j2
└── terraform/
    ├── main.tf                 # Основные ресурсы
    ├── variables.tf            # Переменные
    ├── outputs.tf              # Выходные значения
    ├── providers.tf            # Провайдеры
    └── terraform.tfvars        # Значения переменных (не коммитить!)
🐛 Troubleshooting
Ansible не может подключиться:
bash# Проверь SSH доступ вручную
ssh -i ~/.ssh/your-key.pem ec2-user@<IP>

# Проверь Security Group
aws ec2 describe-security-groups --group-ids <SG_ID>

# Подожди 30-60 секунд после terraform apply
Docker Compose не запускается:
bash# Проверь логи
docker-compose logs

# Проверь Docker service
sudo systemctl status docker

# Пересобери образы
docker-compose build --no-cache
docker-compose up -d
Flask не подключается к PostgreSQL:
bash# Проверь что БД запущена
docker exec postgres_db pg_isready

# Проверь логи
docker logs postgres_db
docker logs web_app

# Проверь переменные окружения
docker exec web_app env | grep DATABASE
Prometheus не собирает метрики:
bash# Проверь targets в Prometheus UI
# http://<IP>:9090/targets

# Проверь что экспортеры доступны
curl http://localhost:9100/metrics
curl http://localhost:8080/metrics

# Проверь конфиг Prometheus
docker exec prometheus cat /etc/prometheus/prometheus.yml
📚 Дополнительные ресурсы

Terraform AWS Provider
Ansible Documentation
Prometheus Documentation
Grafana Documentation
Docker Compose Reference

📝 TODO / Roadmap

 Добавить CI/CD pipeline (GitHub Actions)
 Настроить SSL/TLS через Let's Encrypt
 Добавить Nginx reverse proxy
 Интегрировать с AWS CloudWatch
 Добавить backup для PostgreSQL
 Настроить log aggregation (ELK/Loki)
 Добавить автоматическое scaling
 Переход на Kubernetes (EKS)

👨‍💻 Автор
Учебный проект для изучения DevOps практик
📄 Лицензия
MIT