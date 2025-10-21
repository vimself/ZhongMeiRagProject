"""
应用配置文件
支持开发环境和生产环境的不同配置
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# 加载环境变量
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """基础配置类"""
    
    # Flask配置
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    JSON_AS_ASCII = False  # 支持中文JSON
    
    # 数据库配置
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'rag_knowledge_base')
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        "?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 24))
    JWT_ALGORITHM = 'HS256'
    
    # 文件上传配置
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(basedir, 'uploads'))
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 104857600))  # 100MB
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    
    # 向量数据库配置
    CHROMA_PERSIST_DIRECTORY = os.getenv(
        'CHROMA_PERSIST_DIRECTORY', 
        os.path.join(basedir, 'chroma_db')
    )
    EMBEDDING_MODEL_NAME = os.getenv(
        'EMBEDDING_MODEL_NAME',
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    )
    
    # LLM配置
    LLM_API_BASE = os.getenv('LLM_API_BASE', 'http://localhost:8001/v1')
    LLM_API_KEY = os.getenv('LLM_API_KEY', 'sk-default')
    LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME', 'qwen2-7b-instruct')
    LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS', 2048))
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', 0.7))
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', os.path.join(basedir, 'logs', 'app.log'))
    
    # CORS配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    # 分页配置
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # RAG配置
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    TOP_K = 5
    SIMILARITY_THRESHOLD = 0.7
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        # 创建必要的目录
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    LOG_LEVEL = 'WARNING'
    
    # 生产环境必须设置的配置
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # 确保生产环境密钥已更改
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError('生产环境必须设置安全的SECRET_KEY')


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """获取配置对象"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])

