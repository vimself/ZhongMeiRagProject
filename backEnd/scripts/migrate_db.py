"""
数据库迁移脚本
用于更新数据库结构
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from flask_migrate import Migrate, init, migrate, upgrade


def init_migrations():
    """初始化迁移环境"""
    app = create_app('development')
    
    with app.app_context():
        print('正在初始化迁移环境...')
        os.system('flask db init')
        print('迁移环境初始化完成')


def create_migration(message='Auto migration'):
    """创建迁移脚本"""
    app = create_app('development')
    
    with app.app_context():
        print(f'正在创建迁移脚本: {message}')
        os.system(f'flask db migrate -m "{message}"')
        print('迁移脚本创建完成')


def apply_migrations():
    """应用迁移"""
    app = create_app('development')
    
    with app.app_context():
        print('正在应用数据库迁移...')
        os.system('flask db upgrade')
        print('迁移应用完成')


if __name__ == '__main__':
    print('='* 60)
    print(' RAG知识问答系统 - 数据库迁移工具')
    print('='* 60)
    
    print('\n请选择操作：')
    print('1. 初始化迁移环境 (首次使用)')
    print('2. 创建迁移脚本')
    print('3. 应用迁移')
    print('4. 退出')
    
    choice = input('\n请输入选项 (1-4): ')
    
    if choice == '1':
        init_migrations()
    elif choice == '2':
        message = input('请输入迁移描述: ')
        create_migration(message if message else 'Auto migration')
    elif choice == '3':
        apply_migrations()
    else:
        print('已退出')

