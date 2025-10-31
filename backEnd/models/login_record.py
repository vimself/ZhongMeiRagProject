"""
登录记录模型
"""
from datetime import datetime
from extensions import db
from utils.helpers import get_beijing_now


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
    login_time = db.Column(db.DateTime, default=get_beijing_now)
    logout_time = db.Column(db.DateTime)
    last_login_time = db.Column(db.DateTime, default=get_beijing_now)  # 最后一次登录时间
    login_count = db.Column(db.Integer, default=1)  # 登录次数
    
    # 添加组合索引，用于快速查找相同设备和IP的记录
    __table_args__ = (
        db.Index('idx_user_device_ip', 'user_id', 'device', 'ip'),
    )
    
    def __repr__(self):
        return f'<LoginRecord {self.id}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'device': self.device or 'Unknown',
            'ip': self.ip or '',
            'location': self.location or '未知',
            'loginTime': self.last_login_time.isoformat() if self.last_login_time else (self.login_time.isoformat() if self.login_time else None),
            'status': self.status,
            'userAgent': self.user_agent or '',
            'loginCount': self.login_count or 1
        }

