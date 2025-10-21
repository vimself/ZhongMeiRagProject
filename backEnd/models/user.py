"""
用户模型
"""
from datetime import datetime
from app import db


class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # user, admin
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(255))
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    bio = db.Column(db.String(200))
    status = db.Column(db.String(20), default='active')  # active, disabled
    last_login_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    chat_sessions = db.relationship('ChatSession', backref='user', lazy='dynamic')
    login_records = db.relationship('LoginRecord', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self, include_sensitive=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'role': self.role,
            'email': self.email,
            'phone': self.phone,
            'avatar': self.avatar,
            'department': self.department,
            'position': self.position,
            'bio': self.bio,
            'status': self.status,
            'lastLoginAt': self.last_login_at.isoformat() if self.last_login_at else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
        
        if not include_sensitive and self.phone:
            # 脱敏手机号
            data['phone'] = self.phone[:3] + '****' + self.phone[-4:] if len(self.phone) == 11 else self.phone
        
        return data
    
    def is_admin(self):
        """是否是管理员"""
        return self.role == 'admin'
    
    def is_active(self):
        """是否激活"""
        return self.status == 'active'

