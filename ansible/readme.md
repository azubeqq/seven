tree

ansible/
├── inventory.ini
├── group_vars/
│   └── all.yml
├── playbooks/
│   ├── deploy_app_instance.yml
│   └── deploy_monitoring_instance.yml
└── roles/
    ├── common/              # Общие задачи для всех
    │   └── tasks/
    │       └── main.yml
    ├── docker/              # Установка Docker
    │   └── tasks/
    │       └── main.yml
    ├── flask_app/           # Flask приложение
    │   ├── defaults/
    │   │   └── main.yml
    │   ├── tasks/
    │   │   └── main.yml
    │   ├── templates/
    │   │   └── docker-compose-flask.yml.j2
    │   └── files/
    │       └── app/
    ├── postgresql/          # База данных
    │   ├── defaults/
    │   │   └── main.yml
    │   ├── tasks/
    │   │   └── main.yml
    │   └── templates/
    │       └── docker-compose-postgres.yml.j2
    ├── node_exporter/       # Экспортер метрик хоста
    │   ├── defaults/
    │   │   └── main.yml
    │   ├── tasks/
    │   │   └── main.yml
    │   └── templates/
    │       └── docker-compose-node-exporter.yml.j2
    ├── postgres_exporter/   # Экспортер PostgreSQL
    │   └── tasks/
    │       └── main.yml
    ├── promtail/            # Сборщик логов
    │   ├── defaults/
    │   │   └── main.yml
    │   ├── tasks/
    │   │   └── main.yml
    │   └── templates/
    │       └── promtail-config.yml.j2
    ├── prometheus/          # Мониторинг
    │   ├── defaults/
    │   │   └── main.yml
    │   ├── tasks/
    │   │   └── main.yml
    │   └── templates/
    │       ├── docker-compose-prometheus.yml.j2
    │       ├── prometheus.yml.j2
    │       └── alerts.yml.j2
    ├── grafana/             # Визуализация
    │   ├── defaults/
    │   │   └── main.yml
    │   ├── tasks/
    │   │   └── main.yml
    │   └── templates/
    │       └── docker-compose-grafana.yml.j2
    ├── loki/                # Хранилище логов
    │   ├── defaults/
    │   │   └── main.yml
    │   ├── tasks/
    │   │   └── main.yml
    │   └── templates/
    │       └── loki-config.yml.j2
    └── alertmanager/        # Управление алертами
        └── tasks/
            └── main.yml

