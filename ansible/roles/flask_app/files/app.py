# ========================================
# ФАЙЛ: roles/flask_app/files/app.py
# ========================================
# Flask приложение с:
# - Подключением к PostgreSQL
# - Встроенными Prometheus метриками
# - REST API для работы с данными
# - Health check endpoint
# ========================================

from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import psycopg2
import psycopg2.extras
import os
import logging
from datetime import datetime

# ========================================
# КОНФИГУРАЦИЯ
# ========================================

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создаём Flask приложение
app = Flask(__name__)

# Добавляем Prometheus метрики
# Автоматически создаёт endpoint /metrics
metrics = PrometheusMetrics(app)

# Информация о приложении (доступна в метриках)
metrics.info('app_info', 'Flask Application Info', version='1.0.0')

# ========================================
# DATABASE CONNECTION
# ========================================

def get_db_connection():
    """
    Создаёт подключение к PostgreSQL.
    Параметры берутся из переменных окружения.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST', 'localhost'),
            port=os.getenv('DATABASE_PORT', '5432'),
            dbname=os.getenv('DATABASE_NAME', 'appdb'),
            user=os.getenv('DATABASE_USER', 'appuser'),
            password=os.getenv('DATABASE_PASSWORD', 'password')
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise


def init_database():
    """
    Инициализирует таблицы при первом запуске.
    Создаёт таблицы если их нет.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Таблица пользователей
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица постов
        cur.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                title VARCHAR(200) NOT NULL,
                content TEXT,
                views INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Database tables initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False


# ========================================
# ROUTES - API ENDPOINTS
# ========================================

@app.route('/')
def index():
    """Главная страница с информацией о сервисе."""
    return jsonify({
        'service': 'Flask Monitoring App',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            '/': 'This page',
            '/health': 'Health check',
            '/metrics': 'Prometheus metrics',
            '/users': 'Users API (GET, POST)',
            '/posts': 'Posts API (GET, POST)',
            '/stats': 'Application statistics'
        }
    })


@app.route('/health')
def health_check():
    """
    Health check endpoint.
    Проверяет подключение к базе данных.
    Используется Docker healthcheck и Kubernetes probes.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500


# ----------------------------------------
# USERS API
# ----------------------------------------

@app.route('/users', methods=['GET'])
def get_users():
    """Получить список всех пользователей."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT id, username, email, created_at FROM users ORDER BY created_at DESC")
        users = cur.fetchall()
        cur.close()
        conn.close()
        
        # Конвертируем datetime в строку для JSON
        for user in users:
            user['created_at'] = user['created_at'].isoformat() if user['created_at'] else None
        
        return jsonify(users), 200
    except Exception as e:
        logger.error(f"Get users failed: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/users', methods=['POST'])
def create_user():
    """Создать нового пользователя."""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({'error': 'username and email are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id, username, email, created_at",
            (data['username'], data['email'])
        )
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        user['created_at'] = user['created_at'].isoformat()
        logger.info(f"User created: {user['username']}")
        
        return jsonify(user), 201
    except psycopg2.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 409
    except Exception as e:
        logger.error(f"Create user failed: {e}")
        return jsonify({'error': str(e)}), 500


# ----------------------------------------
# POSTS API
# ----------------------------------------

@app.route('/posts', methods=['GET'])
def get_posts():
    """Получить список всех постов с информацией об авторах."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT p.id, p.title, p.content, p.views, p.created_at,
                   u.username as author
            FROM posts p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
        """)
        posts = cur.fetchall()
        cur.close()
        conn.close()
        
        for post in posts:
            post['created_at'] = post['created_at'].isoformat() if post['created_at'] else None
        
        return jsonify(posts), 200
    except Exception as e:
        logger.error(f"Get posts failed: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/posts', methods=['POST'])
def create_post():
    """Создать новый пост."""
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'title' not in data:
            return jsonify({'error': 'user_id and title are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO posts (user_id, title, content) VALUES (%s, %s, %s) RETURNING id, user_id, title, content, views, created_at",
            (data['user_id'], data['title'], data.get('content', ''))
        )
        post = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        post['created_at'] = post['created_at'].isoformat()
        logger.info(f"Post created: {post['title']}")
        
        return jsonify(post), 201
    except Exception as e:
        logger.error(f"Create post failed: {e}")
        return jsonify({'error': str(e)}), 500


# ----------------------------------------
# STATISTICS
# ----------------------------------------

@app.route('/stats')
def get_stats():
    """Статистика приложения."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("SELECT COUNT(*) as count FROM users")
        users_count = cur.fetchone()['count']
        
        cur.execute("SELECT COUNT(*) as count FROM posts")
        posts_count = cur.fetchone()['count']
        
        cur.execute("SELECT COALESCE(SUM(views), 0) as total FROM posts")
        total_views = cur.fetchone()['total']
        
        cur.close()
        conn.close()
        
        return jsonify({
            'users_count': users_count,
            'posts_count': posts_count,
            'total_views': total_views,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Get stats failed: {e}")
        return jsonify({'error': str(e)}), 500


# ========================================
# STARTUP
# ========================================

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    
    # Инициализируем базу данных
    init_database()
    
    # Запускаем сервер
    app.run(
        host='0.0.0.0',  # Слушаем на всех интерфейсах
        port=5000,       # Порт
        debug=False      # Отключить debug в продакшене
    )
