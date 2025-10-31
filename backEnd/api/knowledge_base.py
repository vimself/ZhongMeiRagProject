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
        
        # 删除相关的向量数据
        try:
            from utils.rag_service import rag_service
            rag_service.delete_collection(kb_id)
            current_app.logger.info(f'删除知识库向量集合: {kb_id}')
        except Exception as e:
            current_app.logger.error(f'删除向量集合失败: {str(e)}', exc_info=True)
            # 继续删除数据库记录
        
        # 删除知识库的所有文档文件
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        documents = Document.query.filter_by(knowledge_base_id=kb_id).all()
        for doc in documents:
            file_path = os.path.join(upload_folder, doc.file_path)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    current_app.logger.warning(f'删除文件失败: {str(e)}')
        
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
        from flask import g
        from werkzeug.utils import secure_filename
        from utils.document_processor import document_processor
        from utils.rag_service import rag_service
        
        # 检查文件
        if 'file' not in request.files:
            return error_response(2001, '未上传文件')
        
        file = request.files['file']
        if file.filename == '':
            return error_response(2001, '文件名为空')
        
        # 获取知识库ID
        kb_id = request.form.get('knowledgeBaseId')
        if not kb_id:
            return error_response(2001, '知识库ID不能为空')
        
        # 验证知识库存在且有权限
        kb = KnowledgeBase.query.get(kb_id)
        if not kb:
            return error_response(2002, '知识库不存在')
        
        if not g.current_user.is_admin():
            permission = KnowledgeBasePermission.query.filter_by(
                knowledge_base_id=kb_id,
                user_id=g.user_id,
                permission='manage'
            ).first()
            if not permission:
                return error_response(403, '无权限管理该知识库')
        
        # 验证文件类型
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'doc', 'docx', 'txt'})
        if file_ext not in allowed_extensions:
            return error_response(2005, f'不支持的文件类型: {file_ext}')
        
        # 保存文件
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        os.makedirs(upload_folder, exist_ok=True)
        
        # 生成唯一文件名
        doc_id = generate_id('doc')
        saved_filename = f"{doc_id}_{filename}"
        file_path = os.path.join(upload_folder, saved_filename)
        
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        current_app.logger.info(f'文件保存成功: {file_path}, 大小: {file_size} 字节')
        
        # 解析文档
        try:
            text = document_processor.extract_text(file_path, file_ext)
            
            if not text or len(text) < 10:
                os.remove(file_path)
                return error_response(2006, '文档内容为空或无法解析')
            
        except Exception as e:
            os.remove(file_path)
            raise Exception(f'文档解析失败: {str(e)}')
        
        # 分块处理
        chunk_size = current_app.config.get('CHUNK_SIZE', 500)
        chunk_overlap = current_app.config.get('CHUNK_OVERLAP', 50)
        
        chunks = document_processor.create_chunks_with_metadata(
            text=text,
            document_id=doc_id,
            document_name=filename,
            kb_id=kb_id,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        current_app.logger.info(f'文档分块完成: {len(chunks)} 个块')
        
        # 向量化并存储到 ChromaDB
        try:
            rag_service.add_documents(kb_id, chunks)
        except Exception as e:
            os.remove(file_path)
            raise Exception(f'向量化存储失败: {str(e)}')
        
        # 保存文档记录到数据库
        document = Document(
            id=doc_id,
            knowledge_base_id=kb_id,
            name=filename,
            file_path=saved_filename,
            file_type=file_ext,
            file_size=file_size,
            status='completed',
            chunk_count=len(chunks),
            uploaded_by=g.user_id,
            uploaded_at=datetime.utcnow()
        )
        
        db.session.add(document)
        
        # 更新知识库的更新时间
        kb.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        current_app.logger.info(f'文档上传成功: {filename} (ID: {doc_id}), 共 {len(chunks)} 个块')
        
        return success_response({
            'documentId': doc_id,
            'documentName': filename,
            'chunkCount': len(chunks),
            'fileSize': file_size
        }, '文档上传成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'上传文档异常: {str(e)}', exc_info=True)
        return error_response(500, f'上传文档失败: {str(e)}')


@knowledge_base_bp.route('/delete-document', methods=['POST'])
@require_auth
def delete_document():
    """
    删除文档
    POST /api/knowledge-base/delete-document
    """
    try:
        from flask import g
        
        data = request.get_json()
        doc_id = data.get('documentId')
        
        if not doc_id:
            return error_response(2001, '文档ID不能为空')
        
        # 查询文档
        document = Document.query.get(doc_id)
        if not document:
            return error_response(2002, '文档不存在')
        
        # 权限检查
        kb = KnowledgeBase.query.get(document.knowledge_base_id)
        if not kb:
            return error_response(2002, '知识库不存在')
        
        if not g.current_user.is_admin():
            permission = KnowledgeBasePermission.query.filter_by(
                knowledge_base_id=document.knowledge_base_id,
                user_id=g.user_id,
                permission='manage'
            ).first()
            if not permission:
                return error_response(403, '无权限管理该知识库')
        
        # 删除 ChromaDB 中的向量数据
        try:
            from utils.rag_service import rag_service
            collection = rag_service.get_or_create_collection(document.knowledge_base_id)
            
            # 删除该文档的所有块
            chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(document.chunk_count or 100)]
            
            # ChromaDB 的 delete 会忽略不存在的 ID，所以直接删除即可
            try:
                collection.delete(ids=chunk_ids)
                current_app.logger.info(f'删除文档向量: {doc_id}')
            except Exception as e:
                current_app.logger.warning(f'删除向量数据失败（可能已不存在）: {str(e)}')
        
        except Exception as e:
            current_app.logger.error(f'删除向量数据异常: {str(e)}', exc_info=True)
            # 继续删除数据库记录
        
        # 删除物理文件
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        file_path = os.path.join(upload_folder, document.file_path)
        
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                current_app.logger.info(f'删除文件: {file_path}')
            except Exception as e:
                current_app.logger.warning(f'删除文件失败: {str(e)}')
        
        # 删除数据库记录
        db.session.delete(document)
        
        # 更新知识库的更新时间
        kb.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        current_app.logger.info(f'删除文档成功: {document.name} (ID: {doc_id})')
        
        return success_response(message='文档删除成功')
        
    except Exception as e:
        db.session.rollback()
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

