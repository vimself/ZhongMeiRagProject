"""
知识库相关模型
"""
from datetime import datetime
from app import db


class KnowledgeBase(db.Model):
    """知识库表"""
    __tablename__ = 'knowledge_bases'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    icon_color = db.Column(db.String(100))
    visible = db.Column(db.String(20), default='all')  # all, authorized, private
    status = db.Column(db.String(20), default='active')  # active, processing, inactive
    progress = db.Column(db.Integer, default=0)
    chunk_size = db.Column(db.Integer, default=500)
    chunk_overlap = db.Column(db.Integer, default=50)
    similarity_threshold = db.Column(db.Float, default=0.7)
    top_k = db.Column(db.Integer, default=5)
    vector_model_id = db.Column(db.String(50))
    created_by = db.Column(db.String(50), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    documents = db.relationship('Document', backref='knowledge_base', lazy='dynamic', cascade='all, delete-orphan')
    permissions = db.relationship('KnowledgeBasePermission', backref='knowledge_base', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<KnowledgeBase {self.name}>'
    
    def to_dict(self, include_stats=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'icon': self.icon,
            'iconColor': self.icon_color,
            'visible': self.visible,
            'status': self.status,
            'progress': self.progress,
            'createdBy': self.created_by,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_stats:
            # 计算文档数量和存储大小
            document_count = self.documents.count()
            total_size = sum([doc.file_size or 0 for doc in self.documents])
            
            data['documentCount'] = document_count
            data['storageSize'] = format_file_size(total_size)
            data['lastUpdate'] = format_relative_time(self.updated_at)
        
        return data


class Document(db.Model):
    """文档表"""
    __tablename__ = 'documents'
    
    id = db.Column(db.String(50), primary_key=True)
    knowledge_base_id = db.Column(db.String(50), db.ForeignKey('knowledge_bases.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.BigInteger)
    file_type = db.Column(db.String(20))  # pdf, doc, docx, txt
    page_count = db.Column(db.Integer)
    chunk_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='processing')  # processing, processed, failed
    error_message = db.Column(db.Text)
    tags = db.Column(db.JSON)
    uploaded_by = db.Column(db.String(50), db.ForeignKey('users.id'))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Document {self.name}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'knowledgeBaseId': self.knowledge_base_id,
            'name': self.name,
            'fileName': self.file_name,
            'size': format_file_size(self.file_size) if self.file_size else '0 B',
            'fileType': self.file_type,
            'pageCount': self.page_count,
            'chunkCount': self.chunk_count,
            'status': self.status,
            'tags': self.tags or [],
            'uploadedBy': self.uploaded_by,
            'uploadTime': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'processedAt': self.processed_at.isoformat() if self.processed_at else None
        }


class KnowledgeBasePermission(db.Model):
    """知识库权限表"""
    __tablename__ = 'knowledge_base_permissions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    knowledge_base_id = db.Column(db.String(50), db.ForeignKey('knowledge_bases.id'), nullable=False, index=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False, index=True)
    permission = db.Column(db.String(20), nullable=False)  # view, manage
    granted_by = db.Column(db.String(50), db.ForeignKey('users.id'))
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 唯一约束
    __table_args__ = (
        db.UniqueConstraint('knowledge_base_id', 'user_id', name='uk_kb_user'),
    )
    
    def __repr__(self):
        return f'<KnowledgeBasePermission kb={self.knowledge_base_id} user={self.user_id}>'


# 工具函数
def format_file_size(size_bytes):
    """格式化文件大小"""
    if size_bytes is None or size_bytes == 0:
        return '0 B'
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f'{size:.2f} {units[unit_index]}'


def format_relative_time(dt):
    """格式化相对时间"""
    if dt is None:
        return ''
    
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days > 365:
        return f'{diff.days // 365}年前'
    elif diff.days > 30:
        return f'{diff.days // 30}个月前'
    elif diff.days > 0:
        return f'{diff.days}天前'
    elif diff.seconds > 3600:
        return f'{diff.seconds // 3600}小时前'
    elif diff.seconds > 60:
        return f'{diff.seconds // 60}分钟前'
    else:
        return '刚刚'

