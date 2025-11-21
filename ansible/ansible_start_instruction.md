# ========================================
# ИНСТРУКЦИЯ ПО ЗАПУСКУ
# ========================================
"""
1. Создание структуры директорий:

mkdir -p ansible/roles/{common,docker,postgres,flask_app,node_exporter,postgres_exporter,prometheus,grafana,alertmanager,loki,promtail}/{defaults,tasks,templates,files,handlers}

2. Копирование всех файлов из артефактов в соответствующие директории

3. Установка Ansible коллекций:

cd ansible
ansible-galaxy collection install community.docker

4. Создание requirements.yml:

cat > requirements.yml << EOF
collections:
  - name: community.docker
    version: ">=3.0.0"
EOF

ansible-galaxy collection install -r requirements.yml

5. Проверка синтаксиса playbook:

ansible-playbook playbooks/deploy.yml --syntax-check

6. Запуск деплоя:

ansible-playbook playbooks/deploy.yml

7. Или с тегами (выборочный деплой):

# Только приложение
ansible-playbook playbooks/deploy.yml --tags app

# Только мониторинг
ansible-playbook playbooks/deploy.yml --tags monitoring

# Только логирование
ansible-playbook playbooks/deploy.yml --tags logging

8. После деплоя:

# Flask App
curl http://<IP>:5000/health

# Prometheus
curl http://<IP>:9090/-/healthy

# Grafana (admin/admin123)
http://<IP>:3000

# Loki
curl http://<IP>:3100/ready
"""
