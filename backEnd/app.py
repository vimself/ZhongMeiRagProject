"""
RAG知识问答系统 - 主应用入口
"""
import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import get_config

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """
    应用工厂函数
    创建并配置Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    config_class.init_app(app)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 配置CORS
    CORS(app, 
         resources={r"/api/*": {
             "origins": app.config['CORS_ORIGINS'],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }})
    
    # 配置日志
    setup_logging(app)
    
    # 注册蓝图
    register_blueprints(app)
    
    # 注册错误处理器
    register_error_handlers(app)
    
    # 健康检查接口
    @app.route('/health', methods=['GET'])
    def health_check():
        """健康检查接口"""
        return jsonify({
            'status': 'healthy',
            'service': 'RAG Knowledge Base API',
            'version': '1.0.0'
        })
    
    return app


def setup_logging(app):
    """配置日志系统"""
    # 创建日志目录
    log_dir = os.path.dirname(app.config['LOG_FILE'])
    os.makedirs(log_dir, exist_ok=True)
    
    # 配置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # 文件处理器
    file_handler = logging.FileHandler(app.config['LOG_FILE'], encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(app.config['LOG_LEVEL'])
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(app.config['LOG_LEVEL'])
    
    # 添加处理器
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    
    app.logger.info(f'应用启动 - 环境: {app.config["ENV"]}')


def register_blueprints(app):
    """注册所有蓝图"""
    from api.auth import auth_bp
    from api.user import user_bp
    from api.dashboard import dashboard_bp
    from api.knowledge_base import knowledge_base_bp
    from api.chat import chat_bp
    from api.search import search_bp
    from api.admin_users import admin_users_bp
    from api.models import models_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(knowledge_base_bp, url_prefix='/api/knowledge-base')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(admin_users_bp, url_prefix='/api/admin/users')
    app.register_blueprint(models_bp, url_prefix='/api/models')
    
    app.logger.info('所有蓝图已注册')


def register_error_handlers(app):
    """注册全局错误处理器"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 400,
            'message': '请求参数错误',
            'body': {}
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 401,
            'message': '未授权，请先登录',
            'body': {}
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 403,
            'message': '权限不足',
            'body': {}
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 404,
            'message': '资源不存在',
            'body': {}
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'服务器内部错误: {str(error)}')
        return jsonify({
            'error': 500,
            'message': '系统异常，请稍后重试',
            'body': {}
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'未处理的异常: {str(error)}', exc_info=True)
        return jsonify({
            'error': 500,
            'message': '系统异常，请稍后重试',
            'body': {}
        }), 500


if __name__ == '__main__':
    app = create_app()
    # 开发环境运行配置
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=app.config['DEBUG']
    )

