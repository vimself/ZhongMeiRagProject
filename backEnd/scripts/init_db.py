"""
数据库初始化脚本
用于创建数据库表和初始数据
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models import User, KnowledgeBase, Model
from utils.helpers import generate_id, hash_password
from datetime import datetime


def init_database():
    """初始化数据库"""
    app = create_app('development')
    
    with app.app_context():
        print('正在创建数据库表...')
        
        # 删除所有表（仅开发环境使用，生产环境慎用！）
        db.drop_all()
        print('已删除旧表')
        
        # 创建所有表
        db.create_all()
        print('数据库表创建完成')
        
        # 插入初始数据
        insert_initial_data()
        
        print('\n数据库初始化完成！')


def insert_initial_data():
    """插入初始数据"""
    print('\n开始插入初始数据...')
    
    # 1. 创建管理员账号
    print('\n[1/3] 创建管理员账号...')
    admin = User(
        id=generate_id('user'),
        username='admin',
        password_hash=hash_password('admin123'),
        name='系统管理员',
        role='admin',
        email='admin@example.com',
        phone='13800138000',
        department='技术部',
        position='系统管理员',
        status='active',
        created_at=datetime.utcnow()
    )
    db.session.add(admin)
    print(f'  - 管理员账号: admin / admin123')
    
    # 2. 创建普通用户账号
    user = User(
        id=generate_id('user'),
        username='user',
        password_hash=hash_password('user123'),
        name='测试用户',
        role='user',
        email='user@example.com',
        phone='13900139000',
        department='产品部',
        position='产品经理',
        status='active',
        created_at=datetime.utcnow()
    )
    db.session.add(user)
    print(f'  - 普通用户账号: user / user123')
    
    db.session.commit()
    print('用户账号创建完成')
    
    # 3. 创建默认模型配置
    print('\n[2/3] 创建默认模型配置...')
    
    # 默认LLM模型
    llm_model = Model(
        id=generate_id('model'),
        name='Qwen2-7B',
        type='llm',
        description='通义千问2代7B模型，适合中文对话和知识问答',
        provider='local',
        endpoint='http://localhost:8001/v1/chat/completions',
        status='offline',
        is_default=True,
        model_size='7B',
        context_length=8192,
        config={
            'temperature': 0.7,
            'topP': 0.9,
            'topK': 40,
            'maxTokens': 2048
        },
        created_at=datetime.utcnow()
    )
    db.session.add(llm_model)
    print('  - 默认LLM模型: Qwen2-7B')
    
    # 默认Embedding模型
    embedding_model = Model(
        id=generate_id('model'),
        name='BGE-M3',
        type='embedding',
        description='BGE-M3中文向量模型，适合RAG检索',
        provider='local',
        endpoint='local',
        status='offline',
        is_default=True,
        model_size='560M',
        context_length=8192,
        config={
            'dimension': 1024,
            'normalize': True
        },
        created_at=datetime.utcnow()
    )
    db.session.add(embedding_model)
    print('  - 默认Embedding模型: BGE-M3')
    
    db.session.commit()
    print('模型配置创建完成')
    
    # 4. 创建示例知识库
    print('\n[3/3] 创建示例知识库...')
    kb = KnowledgeBase(
        id=generate_id('kb'),
        name='技术规范知识库',
        code='TECH_SPEC',
        description='公司技术规范文档集合，包含开发规范、API文档等',
        icon='book',
        icon_color='linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        visible='all',
        status='active',
        progress=100,
        similarity_threshold=0.7,
        top_k=5,
        created_by=admin.id,
        created_at=datetime.utcnow()
    )
    db.session.add(kb)
    print(f'  - 示例知识库: {kb.name}')
    
    db.session.commit()
    print('示例数据创建完成')
    
    print('\n初始数据插入完成！')
    print('\n登录信息：')
    print('=' * 50)
    print('管理员账号: admin / admin123')
    print('普通用户账号: user / user123')
    print('=' * 50)


if __name__ == '__main__':
    print('='* 60)
    print(' RAG知识问答系统 - 数据库初始化')
    print('='* 60)
    
    confirm = input('\n警告：此操作将删除所有现有数据！是否继续？(yes/no): ')
    if confirm.lower() == 'yes':
        init_database()
    else:
        print('已取消操作')

