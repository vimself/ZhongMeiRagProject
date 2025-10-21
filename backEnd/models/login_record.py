"""
登录记录模型
"""
from datetime import datetime
from app import db


class LoginRecord(db.Model):
    """登录记录表"""
    __tablename__ = 'login_records'
    
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False, index=True)
    ip = db.Column(db.String(50))
    location = db.Column(db.String(100))
    device = db.Column(db.String(100))
    user_agent = db.Column(db.String(500))
    status = db.Column(db.String(20), default='current')  # current, ended
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<LoginRecord {self.id}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'device': self.device or 'Unknown',
            'ip': self.ip or '',
            'location': self.location or '未知',
            'loginTime': self.login_time.isoformat() if self.login_time else None,
            'status': self.status,
            'userAgent': self.user_agent or ''
        }

