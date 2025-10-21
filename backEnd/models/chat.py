"""
对话相关模型
"""
from datetime import datetime
from app import db


class ChatSession(db.Model):
    """会话表"""
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), default='新对话')
    knowledge_base_id = db.Column(db.String(50), db.ForeignKey('knowledge_bases.id'))
    model_id = db.Column(db.String(50), db.ForeignKey('models.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    messages = db.relationship('ChatMessage', backref='session', lazy='dynamic', cascade='all, delete-orphan', order_by='ChatMessage.created_at')
    
    def __repr__(self):
        return f'<ChatSession {self.id}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'knowledgeBaseId': self.knowledge_base_id,
            'modelId': self.model_id,
            'time': format_chat_time(self.created_at),
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }


class ChatMessage(db.Model):
    """消息表"""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.String(50), primary_key=True)
    session_id = db.Column(db.String(50), db.ForeignKey('chat_sessions.id'), nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False)  # user, assistant
    content = db.Column(db.Text, nullable=False)
    references = db.Column(db.JSON)  # 引用来源（JSON格式）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatMessage {self.id}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'sessionId': self.session_id,
            'role': self.role,
            'content': self.content,
            'references': self.references or [],
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }


def format_chat_time(dt):
    """格式化聊天时间"""
    if dt is None:
        return ''
    
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days == 0:
        return f'今天 {dt.strftime("%H:%M")}'
    elif diff.days == 1:
        return f'昨天 {dt.strftime("%H:%M")}'
    elif diff.days < 7:
        return f'{diff.days}天前'
    else:
        return dt.strftime('%Y-%m-%d')

