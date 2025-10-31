"""
模型相关模型
"""
from datetime import datetime
from extensions import db


class Model(db.Model):
    """模型表"""
    __tablename__ = 'models'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    type = db.Column(db.String(20), nullable=False)  # llm, embedding
    description = db.Column(db.Text)
    provider = db.Column(db.String(50))  # local, openai, etc.
    endpoint = db.Column(db.String(500))
    api_key = db.Column(db.String(255))
    status = db.Column(db.String(20), default='offline')  # online, offline, error
    is_default = db.Column(db.Boolean, default=False)
    
    # 模型参数
    model_size = db.Column(db.String(50))
    context_length = db.Column(db.Integer)
    gpu_memory = db.Column(db.String(50))
    
    # 配置参数（JSON格式）
    config = db.Column(db.JSON)
    
    # 健康检查
    last_check_time = db.Column(db.DateTime)
    response_time = db.Column(db.Integer)  # 毫秒
    health_message = db.Column(db.String(500))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Model {self.name}>'
    
    def to_dict(self, include_sensitive=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'provider': self.provider,
            'endpoint': self.endpoint,
            'status': self.status,
            'isDefault': self.is_default,
            'modelSize': self.model_size,
            'contextLength': self.context_length,
            'gpuMemory': self.gpu_memory,
            'config': self.config or {},
            'healthCheck': {
                'lastCheckTime': self.last_check_time.isoformat() if self.last_check_time else None,
                'responseTime': self.response_time,
                'status': self.status,
                'message': self.health_message or ''
            },
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # 不返回敏感信息
        if not include_sensitive:
            data.pop('apiKey', None)
        else:
            data['apiKey'] = self.api_key
        
        return data
    
    def get_latency_str(self):
        """获取延迟字符串"""
        if self.response_time is None:
            return '-'
        return f'{self.response_time}ms'

