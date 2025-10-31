#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
登录记录表迁移脚本
添加 last_login_time 和 login_count 字段
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from sqlalchemy import text
from datetime import datetime

def migrate_login_records():
    """迁移登录记录表"""
    app = create_app()
    
    with app.app_context():
        try:
            print('开始迁移登录记录表...')
            
            # 检查字段是否已存在
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('login_records')]
            
            # 添加新字段
            if 'last_login_time' not in columns:
                print('添加 last_login_time 字段...')
                with db.engine.connect() as conn:
                    conn.execute(text(
                        'ALTER TABLE login_records ADD COLUMN last_login_time DATETIME DEFAULT NULL'
                    ))
                    conn.commit()
                    
                    # 将现有记录的 last_login_time 设置为 login_time
                    conn.execute(text(
                        'UPDATE login_records SET last_login_time = login_time WHERE last_login_time IS NULL'
                    ))
                    conn.commit()
                print('✓ last_login_time 字段添加成功')
            else:
                print('✓ last_login_time 字段已存在')
            
            if 'login_count' not in columns:
                print('添加 login_count 字段...')
                with db.engine.connect() as conn:
                    conn.execute(text(
                        'ALTER TABLE login_records ADD COLUMN login_count INT DEFAULT 1'
                    ))
                    conn.commit()
                    
                    # 将现有记录的 login_count 设置为 1
                    conn.execute(text(
                        'UPDATE login_records SET login_count = 1 WHERE login_count IS NULL'
                    ))
                    conn.commit()
                print('✓ login_count 字段添加成功')
            else:
                print('✓ login_count 字段已存在')
            
            # 创建组合索引
            try:
                print('创建组合索引 idx_user_device_ip...')
                with db.engine.connect() as conn:
                    conn.execute(text(
                        'CREATE INDEX idx_user_device_ip ON login_records (user_id, device, ip)'
                    ))
                    conn.commit()
                print('✓ 组合索引创建成功')
            except Exception as e:
                error_msg = str(e).lower()
                if 'duplicate' in error_msg or 'already exists' in error_msg or 'exist' in error_msg:
                    print('✓ 组合索引已存在')
                else:
                    print(f'⚠ 创建索引时出现警告: {str(e)}')
            
            print('\n✅ 登录记录表迁移完成！')
            print('\n注意事项：')
            print('1. 现有的登录记录已设置初始值')
            print('2. 相同设备和IP的新登录将更新已有记录')
            print('3. 建议重启后端服务以应用更改')
            
        except Exception as e:
            print(f'\n❌ 迁移失败: {str(e)}')
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    migrate_login_records()

