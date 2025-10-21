"""
知识库管理模块API
包含知识库CRUD、文档管理等接口
"""
from flask import Blueprint, request, current_app, send_file
from models.knowledge_base import KnowledgeBase, Document, KnowledgeBasePermission
from models.model import Model
from utils.auth import require_auth, require_admin
from utils.response import success_response, error_response
from utils.helpers import generate_id, paginate
from app import db
from datetime import datetime
import os

knowledge_base_bp = Blueprint('knowledge_base', __name__)


@knowledge_base_bp.route('/stats', methods=['POST'])
@require_auth
def get_stats():
    """
    获取知识库统计
    POST /api/knowledge-base/stats
    """
    try:
        from flask import g
        
        # 可访问的知识库数量
        if g.current_user.is_admin():
            accessible_kb = KnowledgeBase.query.count()
            accessible_docs = Document.query.count()
        else:
            # 普通用户：计算有权限的知识库
            accessible_kb = KnowledgeBase.query.filter(
                (KnowledgeBase.visible == 'all') |
                (KnowledgeBase.id.in_(
                    db.session.query(KnowledgeBasePermission.knowledge_base_id)
                    .filter_by(user_id=g.user_id)
                ))
            ).count()
            
            # 可访问的文档数
            accessible_kb_ids = [kb.id for kb in KnowledgeBase.query.filter(
                (KnowledgeBase.visible == 'all') |
                (KnowledgeBase.id.in_(
                    db.session.query(KnowledgeBasePermission.knowledge_base_id)
                    .filter_by(user_id=g.user_id)
                ))
            ).all()]
            accessible_docs = Document.query.filter(
                Document.knowledge_base_id.in_(accessible_kb_ids)
            ).count() if accessible_kb_ids else 0
        
        # 今日提问数（暂时返回0）
        today_questions = 0
        
        stats = {
            'accessibleKnowledgeBase': accessible_kb,
            'accessibleDocuments': accessible_docs,
            'todayQuestions': today_questions
        }
        
        return success_response(stats)
        
    except Exception as e:
        current_app.logger.error(f'获取知识库统计异常: {str(e)}', exc_info=True)
        return error_response(500, '获取统计数据失败')


@knowledge_base_bp.route('/list', methods=['POST'])
@require_auth
def get_list():
    """
    获取知识库列表
    POST /api/knowledge-base/list
    """
    try:
        from flask import g
        data = request.get_json() or {}
        
        page = int(data.get('page', 1))
        page_size = int(data.get('pageSize', 20))
        keyword = data.get('keyword', '').strip()
        
        # 构建查询
        query = KnowledgeBase.query
        
        # 权限过滤
        if not g.current_user.is_admin():
            # 普通用户只能看到：公开的 + 授权的
            query = query.filter(
                (KnowledgeBase.visible == 'all') |
                (KnowledgeBase.id.in_(
                    db.session.query(KnowledgeBasePermission.knowledge_base_id)
                    .filter_by(user_id=g.user_id)
                ))
            )
        
        # 关键词搜索
        if keyword:
            query = query.filter(
                (KnowledgeBase.name.like(f'%{keyword}%')) |
                (KnowledgeBase.description.like(f'%{keyword}%'))
            )
        
        # 排序
        query = query.order_by(KnowledgeBase.updated_at.desc())
        
        # 分页
        result = paginate(query, page, page_size)
        
        # 添加统计信息
        for item in result['list']:
            kb = KnowledgeBase.query.get(item['id'])
            if kb:
                item['documentCount'] = kb.documents.count()
                item['storageSize'] = format_storage_size(kb)
                item['lastUpdate'] = format_relative_time(kb.updated_at)
                item['viewers'] = get_kb_viewers(kb)
                item['tags'] = []
        
        return success_response(result)
        
    except Exception as e:
        current_app.logger.error(f'获取知识库列表异常: {str(e)}', exc_info=True)
        return error_response(500, '获取知识库列表失败')


@knowledge_base_bp.route('/detail', methods=['POST'])
@require_auth
def get_detail():
    """
    获取知识库详情
    POST /api/knowledge-base/detail
    """
    try:
        from flask import g
        data = request.get_json()
        
        kb_id = data.get('id')
        if not kb_id:
            return error_response(2001, '知识库ID不能为空')
        
        kb = KnowledgeBase.query.get(kb_id)
        if not kb:
            return error_response(2002, '知识库不存在')
        
        # 权限检查
        if not g.current_user.is_admin():
            if kb.visible != 'all':
                permission = KnowledgeBasePermission.query.filter_by(
                    knowledge_base_id=kb_id,
                    user_id=g.user_id
                ).first()
                if not permission:
                    return error_response(403, '无权限访问该知识库')
        
        # 构建响应数据
        detail = kb.to_dict()
        detail['storageSize'] = format_storage_size(kb)
        detail['viewers'] = get_kb_viewers(kb)
        
        # 权限信息
        if g.current_user.is_admin():
            detail['permission'] = 'manage'
        else:
            permission = KnowledgeBasePermission.query.filter_by(
                knowledge_base_id=kb_id,
                user_id=g.user_id
            ).first()
            detail['permission'] = permission.permission if permission else 'view'
        
        return success_response(detail)
        
    except Exception as e:
        current_app.logger.error(f'获取知识库详情异常: {str(e)}', exc_info=True)
        return error_response(500, '获取知识库详情失败')


@knowledge_base_bp.route('/create', methods=['POST'])
@require_admin
def create():
    """
    创建知识库（简化版）
    POST /api/knowledge-base/create
    """
    try:
        from flask import g
        data = request.get_json()
        
        # 获取参数
        name = data.get('name', '').strip()
        code = data.get('code', '').strip()
        description = data.get('description', '').strip()
        visible = data.get('visible', 'all')
        
        # 参数验证
        if not name or not code:
            return error_response(2001, '知识库名称和编码不能为空')
        
        # 检查编码是否已存在
        existing = KnowledgeBase.query.filter_by(code=code).first()
        if existing:
            return error_response(2003, '知识库编码已存在')
        
        # 创建知识库
        kb = KnowledgeBase(
            id=generate_id('kb'),
            name=name,
            code=code,
            description=description,
            visible=visible,
            status='active',
            created_by=g.user_id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(kb)
        db.session.commit()
        
        current_app.logger.info(f'创建知识库: {name} (ID: {kb.id})')
        
        return success_response(kb.to_dict(), '知识库创建成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'创建知识库异常: {str(e)}', exc_info=True)
        return error_response(500, '创建知识库失败')


@knowledge_base_bp.route('/update', methods=['POST'])
@require_auth
def update():
    """
    更新知识库
    POST /api/knowledge-base/update
    """
    try:
        from flask import g
        data = request.get_json()
        
        kb_id = data.get('id')
        if not kb_id:
            return error_response(2001, '知识库ID不能为空')
        
        kb = KnowledgeBase.query.get(kb_id)
        if not kb:
            return error_response(2002, '知识库不存在')
        
        # 权限检查（需要管理权限）
        if not g.current_user.is_admin():
            permission = KnowledgeBasePermission.query.filter_by(
                knowledge_base_id=kb_id,
                user_id=g.user_id,
                permission='manage'
            ).first()
            if not permission:
                return error_response(403, '无权限管理该知识库')
        
        # 更新字段
        if 'name' in data:
            kb.name = data['name'].strip()
        if 'description' in data:
            kb.description = data['description'].strip()
        if 'similarityThreshold' in data:
            kb.similarity_threshold = float(data['similarityThreshold'])
        
        kb.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        current_app.logger.info(f'更新知识库: {kb.name} (ID: {kb_id})')
        
        return success_response(kb.to_dict(), '知识库更新成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'更新知识库异常: {str(e)}', exc_info=True)
        return error_response(500, '更新知识库失败')


@knowledge_base_bp.route('/delete', methods=['POST'])
@require_admin
def delete():
    """
    删除知识库
    POST /api/knowledge-base/delete
    """
    try:
        data = request.get_json()
        
        kb_id = data.get('id')
        if not kb_id:
            return error_response(2001, '知识库ID不能为空')
        
        kb = KnowledgeBase.query.get(kb_id)
        if not kb:
            return error_response(2002, '知识库不存在')
        
        # TODO: 删除相关的向量数据
        
        # 删除知识库（级联删除文档和权限）
        db.session.delete(kb)
        db.session.commit()
        
        current_app.logger.info(f'删除知识库: {kb.name} (ID: {kb_id})')
        
        return success_response(message='知识库删除成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'删除知识库异常: {str(e)}', exc_info=True)
        return error_response(500, '删除知识库失败')


@knowledge_base_bp.route('/documents', methods=['POST'])
@require_auth
def get_documents():
    """
    获取文档列表
    POST /api/knowledge-base/documents
    """
    try:
        from flask import g
        data = request.get_json()
        
        kb_id = data.get('knowledgeBaseId')
        if not kb_id:
            return error_response(2001, '知识库ID不能为空')
        
        # 权限检查
        kb = KnowledgeBase.query.get(kb_id)
        if not kb:
            return error_response(2002, '知识库不存在')
        
        if not g.current_user.is_admin():
            if kb.visible != 'all':
                permission = KnowledgeBasePermission.query.filter_by(
                    knowledge_base_id=kb_id,
                    user_id=g.user_id
                ).first()
                if not permission:
                    return error_response(403, '无权限访问该知识库')
        
        # 分页参数
        page = int(data.get('page', 1))
        page_size = int(data.get('pageSize', 20))
        
        # 查询文档
        query = Document.query.filter_by(knowledge_base_id=kb_id)\
            .order_by(Document.uploaded_at.desc())
        
        result = paginate(query, page, page_size)
        
        return success_response(result)
        
    except Exception as e:
        current_app.logger.error(f'获取文档列表异常: {str(e)}', exc_info=True)
        return error_response(500, '获取文档列表失败')


@knowledge_base_bp.route('/upload-document', methods=['POST'])
@require_auth
def upload_document():
    """
    上传文档
    POST /api/knowledge-base/upload-document
    """
    try:
        # TODO: 实现文档上传和处理逻辑
        return error_response(2004, '文档上传功能开发中')
        
    except Exception as e:
        current_app.logger.error(f'上传文档异常: {str(e)}', exc_info=True)
        return error_response(500, '上传文档失败')


@knowledge_base_bp.route('/delete-document', methods=['POST'])
@require_auth
def delete_document():
    """
    删除文档
    POST /api/knowledge-base/delete-document
    """
    try:
        # TODO: 实现文档删除逻辑
        return error_response(2004, '文档删除功能开发中')
        
    except Exception as e:
        current_app.logger.error(f'删除文档异常: {str(e)}', exc_info=True)
        return error_response(500, '删除文档失败')


@knowledge_base_bp.route('/document-preview', methods=['POST'])
@require_auth
def document_preview():
    """
    获取文档预览
    POST /api/knowledge-base/document-preview
    """
    try:
        # TODO: 实现文档预览功能
        return error_response(2004, '文档预览功能开发中')
        
    except Exception as e:
        current_app.logger.error(f'获取文档预览异常: {str(e)}', exc_info=True)
        return error_response(500, '获取文档预览失败')


@knowledge_base_bp.route('/export-documents', methods=['POST'])
@require_auth
def export_documents():
    """
    批量导出文档
    POST /api/knowledge-base/export-documents
    """
    try:
        # TODO: 实现文档导出功能
        return error_response(2004, '文档导出功能开发中')
        
    except Exception as e:
        current_app.logger.error(f'导出文档异常: {str(e)}', exc_info=True)
        return error_response(500, '导出文档失败')


@knowledge_base_bp.route('/vector-models', methods=['POST'])
@require_admin
def get_vector_models():
    """
    获取向量模型列表
    POST /api/knowledge-base/vector-models
    """
    try:
        models = Model.query.filter_by(type='embedding').all()
        models_data = [m.to_dict() for m in models]
        
        return success_response(models_data)
        
    except Exception as e:
        current_app.logger.error(f'获取向量模型列表异常: {str(e)}', exc_info=True)
        return error_response(500, '获取向量模型列表失败')


# 辅助函数
def format_storage_size(kb):
    """格式化存储大小"""
    total_size = sum([doc.file_size or 0 for doc in kb.documents])
    if total_size == 0:
        return '0 B'
    
    units = ['B', 'KB', 'MB', 'GB']
    unit_index = 0
    size = float(total_size)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f'{size:.1f} {units[unit_index]}'


def format_relative_time(dt):
    """格式化相对时间"""
    if not dt:
        return ''
    
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days > 30:
        return f'{diff.days // 30}个月前'
    elif diff.days > 0:
        return f'{diff.days}天前'
    elif diff.seconds > 3600:
        return f'{diff.seconds // 3600}小时前'
    elif diff.seconds > 60:
        return f'{diff.seconds // 60}分钟前'
    else:
        return '刚刚'


def get_kb_viewers(kb):
    """获取知识库查看人数"""
    # 简化版：返回权限用户数 + 1（创建者）
    if kb.visible == 'all':
        return 0  # 全员可见
    
    count = KnowledgeBasePermission.query.filter_by(
        knowledge_base_id=kb.id
    ).count()
    
    return count

