from flask import Flask, jsonify
from flask_cors import CORS
from config.env import Config
from src.database import db
from src.container import Container
from src.controllers.task_controller import task_bp
from src.controllers.user_controller import user_bp
from src.controllers.report_controller import report_bp
import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    container = Container()
    app.container = container

    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)

    @app.route('/health')
    def health():
        return jsonify({'status': 'ok', 'timestamp': str(datetime.datetime.now())})

    @app.route('/')
    def index():
        return jsonify({'message': 'Task Manager API (Refactored)', 'version': '2.0'})

    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({'error': 'Internal server error'}), 500

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5002)
