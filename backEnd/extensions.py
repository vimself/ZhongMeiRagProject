"""
Flask扩展实例
将扩展实例与app解耦，避免循环导入
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 初始化扩展实例
db = SQLAlchemy()
migrate = Migrate()

