from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from prometheus_flask_exporter import PrometheusMetrics
import os
import time
import socket

app = Flask(__name__)

cache_config = {
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_HOST": os.environ.get('REDIS_HOST'),
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 0,
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(cache_config)

db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')
db_host = 'db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)
metrics = PrometheusMetrics(app)

@app.route('/health')
def health_check():
    return jsonify(status="OK"), 200

@app.route('/report')
@cache.cached(timeout=30)
def get_report():
    time.sleep(3)
    report_data = {
        'generated_at': time.time(),
        'message': 'Это очень долгий отчет, который теперь кэшируется.'
    }
    return jsonify(report_data)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'username' in data or not 'email' in data:
        return jsonify({'message': 'Не предоставлены username или email'}), 400
    
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Пользователь успешно создан'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(users_list)

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    
    db.session.commit()
    return jsonify({'message': 'Данные пользователя успешно обновлены'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Пользователь успешно удален'})


@app.route('/')
def index():
    hostname = socket.gethostname()
    return f"API работает. Запрос обработан контейнером: {hostname}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)