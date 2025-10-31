"""
Pytest配置和共享fixtures
遵循pytest最佳实践
"""
import pytest
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions import db
from models.user import User
from models.knowledge_base import KnowledgeBase, Document
from models.model import Model
from models.chat import ChatSession
from utils.helpers import generate_id, hash_password
from utils.auth import generate_token


@pytest.fixture(scope='session')
def app():
    """创建测试应用实例（session级别）"""
    app = create_app('testing')
    return app


@pytest.fixture(scope='function')
def client(app):
    """创建测试客户端（function级别，每个测试独立）"""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """创建测试数据库会话（function级别）"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        yield db
        
        # 测试后清理
        db.session.remove()
        db.drop_all()


@pytest.fixture
def admin_user(db_session):
    """创建管理员用户fixture"""
    user = User(
        id=generate_id('user'),
        username='admin',
        password_hash=hash_password('Admin123!'),
        name='管理员',
        email='admin@example.com',
        phone='13800138000',
        role='admin',
        status='active',
        created_at=datetime.utcnow()
    )
    db_session.session.add(user)
    db_session.session.commit()
    return user


@pytest.fixture
def normal_user(db_session):
    """创建普通用户fixture"""
    user = User(
        id=generate_id('user'),
        username='testuser',
        password_hash=hash_password('Test123!'),
        name='测试用户',
        email='test@example.com',
        phone='13900139000',
        role='user',
        status='active',
        created_at=datetime.utcnow()
    )
    db_session.session.add(user)
    db_session.session.commit()
    return user


@pytest.fixture
def disabled_user(db_session):
    """创建已禁用用户fixture"""
    user = User(
        id=generate_id('user'),
        username='disabled',
        password_hash=hash_password('Disabled123!'),
        name='禁用用户',
        email='disabled@example.com',
        role='user',
        status='disabled',
        created_at=datetime.utcnow()
    )
    db_session.session.add(user)
    db_session.session.commit()
    return user


@pytest.fixture
def admin_token(app, admin_user):
    """生成管理员token"""
    with app.app_context():
        return generate_token(admin_user.id)


@pytest.fixture
def user_token(app, normal_user):
    """生成普通用户token"""
    with app.app_context():
        return generate_token(normal_user.id)


@pytest.fixture
def auth_headers_admin(admin_token):
    """管理员认证头"""
    return {'Authorization': f'Bearer {admin_token}'}


@pytest.fixture
def auth_headers_user(user_token):
    """普通用户认证头"""
    return {'Authorization': f'Bearer {user_token}'}


@pytest.fixture
def knowledge_base(db_session, admin_user):
    """创建测试知识库"""
    kb = KnowledgeBase(
        id=generate_id('kb'),
        name='测试知识库',
        code='test_kb',
        description='用于测试的知识库',
        visible='all',
        status='active',
        created_by=admin_user.id,
        created_at=datetime.utcnow()
    )
    db_session.session.add(kb)
    db_session.session.commit()
    return kb


@pytest.fixture
def llm_model(db_session):
    """创建LLM模型"""
    model = Model(
        id=generate_id('model'),
        name='测试LLM模型',
        type='llm',
        description='测试用LLM模型',
        provider='openai',
        endpoint='http://localhost:8001/v1',
        status='online',
        is_default=True,
        created_at=datetime.utcnow()
    )
    db_session.session.add(model)
    db_session.session.commit()
    return model


@pytest.fixture
def embedding_model(db_session):
    """创建Embedding模型"""
    model = Model(
        id=generate_id('model'),
        name='测试Embedding模型',
        type='embedding',
        description='测试用Embedding模型',
        provider='local',
        endpoint='local',
        status='online',
        is_default=True,
        created_at=datetime.utcnow()
    )
    db_session.session.add(model)
    db_session.session.commit()
    return model


@pytest.fixture
def chat_session(db_session, normal_user, knowledge_base, llm_model):
    """创建聊天会话"""
    session = ChatSession(
        id=generate_id('session'),
        user_id=normal_user.id,
        title='测试对话',
        knowledge_base_id=knowledge_base.id,
        model_id=llm_model.id,
        created_at=datetime.utcnow()
    )
    db_session.session.add(session)
    db_session.session.commit()
    return session


@pytest.fixture(autouse=True)
def reset_db(db_session):
    """每个测试后自动清理数据库"""
    yield
    # 测试后清理所有数据
    db_session.session.rollback()


