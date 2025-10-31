"""
智能问答模块API
包含会话管理、消息发送等接口
"""
from flask import Blueprint, request, current_app
from models.knowledge_base import KnowledgeBase, KnowledgeBasePermission
from models.model import Model
from models.chat import ChatSession, ChatMessage
from utils.auth import require_auth
from utils.response import success_response, error_response
from utils.helpers import generate_id, get_beijing_now
from extensions import db
from datetime import datetime

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/knowledge-bases', methods=['POST'])
@require_auth
def get_knowledge_bases():
    """
    获取知识库列表（对话用）
    POST /api/chat/knowledge-bases
    """
    try:
        from flask import g
        
        # 查询用户可访问的知识库
        if g.current_user.is_admin():
            kbs = KnowledgeBase.query.filter_by(status='active').all()
        else:
            kbs = KnowledgeBase.query.filter(
                KnowledgeBase.status == 'active',
                (KnowledgeBase.visible == 'all') |
                (KnowledgeBase.id.in_(
                    db.session.query(KnowledgeBasePermission.knowledge_base_id)
                    .filter_by(user_id=g.user_id)
                ))
            ).all()
        
        kb_list = [{'id': kb.id, 'name': kb.name} for kb in kbs]
        
        return success_response(kb_list)
        
    except Exception as e:
        current_app.logger.error(f'获取知识库列表异常: {str(e)}', exc_info=True)
        return error_response(500, '获取知识库列表失败')


@chat_bp.route('/models', methods=['POST'])
@require_auth
def get_models():
    """
    获取模型列表
    POST /api/chat/models
    """
    try:
        # 查询在线的LLM模型
        models = Model.query.filter_by(type='llm', status='online').all()
        
        model_list = [
            {
                'id': m.id,
                'name': m.name,
                'description': m.description or ''
            }
            for m in models
        ]
        
        # 如果没有在线模型，返回所有LLM模型
        if not model_list:
            models = Model.query.filter_by(type='llm').all()
            model_list = [
                {
                    'id': m.id,
                    'name': m.name,
                    'description': m.description or ''
                }
                for m in models
            ]
        
        return success_response(model_list)
        
    except Exception as e:
        current_app.logger.error(f'获取模型列表异常: {str(e)}', exc_info=True)
        return error_response(500, '获取模型列表失败')


@chat_bp.route('/sessions', methods=['POST'])
@require_auth
def get_sessions():
    """
    获取会话历史
    POST /api/chat/sessions
    """
    try:
        from flask import g
        data = request.get_json() or {}
        
        limit = int(data.get('limit', 20))
        limit = min(max(1, limit), 100)
        
        # 查询用户的会话
        sessions = ChatSession.query.filter_by(user_id=g.user_id)\
            .order_by(ChatSession.updated_at.desc())\
            .limit(limit)\
            .all()
        
        sessions_data = [s.to_dict() for s in sessions]
        
        return success_response(sessions_data)
        
    except Exception as e:
        current_app.logger.error(f'获取会话历史异常: {str(e)}', exc_info=True)
        return error_response(500, '获取会话历史失败')


@chat_bp.route('/session/create', methods=['POST'])
@require_auth
def create_session():
    """
    创建会话
    POST /api/chat/session/create
    """
    try:
        from flask import g
        data = request.get_json()
        
        knowledge_base_id = data.get('knowledgeBaseId')
        model_id = data.get('modelId')
        
        # 参数验证
        if not knowledge_base_id or not model_id:
            return error_response(3001, '知识库和模型不能为空')
        
        # 创建会话
        session = ChatSession(
            id=generate_id('session'),
            user_id=g.user_id,
            title='新对话',
            knowledge_base_id=knowledge_base_id if knowledge_base_id != 'all' else None,
            model_id=model_id,
            created_at=get_beijing_now()
        )
        
        db.session.add(session)
        db.session.commit()
        
        current_app.logger.info(f'创建会话: {session.id}')
        
        return success_response(session.to_dict(), '会话创建成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'创建会话异常: {str(e)}', exc_info=True)
        return error_response(500, '创建会话失败')


@chat_bp.route('/message/send', methods=['POST'])
@require_auth
def send_message():
    """
    发送消息
    POST /api/chat/message/send
    """
    try:
        from flask import g
        data = request.get_json()
        
        session_id = data.get('sessionId')
        question = data.get('question', '').strip()
        
        # 参数验证
        if not session_id or not question:
            return error_response(3001, '会话ID和问题不能为空')
        
        if len(question) > 1000:
            return error_response(3002, '问题长度不能超过1000字符')
        
        # 查询会话
        session = ChatSession.query.get(session_id)
        if not session:
            return error_response(3003, '会话不存在')
        
        # 权限检查
        if session.user_id != g.user_id:
            return error_response(403, '无权限访问该会话')
        
        # 保存用户消息
        user_message = ChatMessage(
            id=generate_id('msg'),
            session_id=session_id,
            role='user',
            content=question,
            created_at=get_beijing_now()
        )
        db.session.add(user_message)
        
        # 调用 RAG 引擎生成答案
        try:
            from utils.rag_service import rag_service
            from models.model import Model
            
            # 获取模型信息
            model = Model.query.get(session.model_id)
            model_name = model.name if model else None
            
            # 获取知识库配置
            kb_id = session.knowledge_base_id
            similarity_threshold = current_app.config.get('SIMILARITY_THRESHOLD', 0.7)
            top_k = current_app.config.get('TOP_K', 5)
            
            # 如果知识库有自定义阈值，使用知识库的配置
            if kb_id:
                kb = KnowledgeBase.query.get(kb_id)
                if kb and kb.similarity_threshold:
                    similarity_threshold = kb.similarity_threshold
            
            # 调用 RAG 服务
            rag_result = rag_service.chat(
                question=question,
                kb_id=kb_id,
                model_name=model_name,
                top_k=top_k,
                similarity_threshold=similarity_threshold
            )
            
            answer = rag_result['answer']
            references = rag_result['references']
            
            current_app.logger.info(
                f'RAG 回答成功: session={session_id}, '
                f'context_count={rag_result.get("context_count", 0)}'
            )
            
        except Exception as e:
            current_app.logger.error(f'RAG 回答失败: {str(e)}', exc_info=True)
            answer = '抱歉，生成回答时出现了问题。请稍后重试或联系管理员。'
            references = []
        
        # 保存助手消息
        assistant_message = ChatMessage(
            id=generate_id('msg'),
            session_id=session_id,
            role='assistant',
            content=answer,
            references=references,
            created_at=get_beijing_now()
        )
        db.session.add(assistant_message)
        
        # 更新会话时间
        session.updated_at = get_beijing_now()
        
        # 自动生成会话标题（第一条消息）
        if session.messages.count() == 0:
            session.title = question[:20] + ('...' if len(question) > 20 else '')
        
        db.session.commit()
        
        current_app.logger.info(f'发送消息: session={session_id}')
        
        return success_response({
            'answer': answer,
            'references': references
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'发送消息异常: {str(e)}', exc_info=True)
        return error_response(500, '发送消息失败')


@chat_bp.route('/session/messages', methods=['POST'])
@require_auth
def get_session_messages():
    """
    获取会话消息
    POST /api/chat/session/messages
    """
    try:
        from flask import g
        data = request.get_json()
        
        session_id = data.get('sessionId')
        if not session_id:
            return error_response(3001, '会话ID不能为空')
        
        # 查询会话
        session = ChatSession.query.get(session_id)
        if not session:
            return error_response(3003, '会话不存在')
        
        # 权限检查
        if session.user_id != g.user_id:
            return error_response(403, '无权限访问该会话')
        
        # 查询消息
        messages = ChatMessage.query.filter_by(session_id=session_id)\
            .order_by(ChatMessage.created_at.asc())\
            .all()
        
        messages_data = [m.to_dict() for m in messages]
        
        return success_response(messages_data)
        
    except Exception as e:
        current_app.logger.error(f'获取会话消息异常: {str(e)}', exc_info=True)
        return error_response(500, '获取会话消息失败')


@chat_bp.route('/session/delete', methods=['POST'])
@require_auth
def delete_session():
    """
    删除会话
    POST /api/chat/session/delete
    """
    try:
        from flask import g
        data = request.get_json()
        
        session_id = data.get('sessionId')
        if not session_id:
            return error_response(3001, '会话ID不能为空')
        
        # 查询会话
        session = ChatSession.query.get(session_id)
        if not session:
            return error_response(3003, '会话不存在')
        
        # 权限检查
        if session.user_id != g.user_id:
            return error_response(403, '无权限删除该会话')
        
        # 删除会话（级联删除消息）
        db.session.delete(session)
        db.session.commit()
        
        current_app.logger.info(f'删除会话: {session_id}')
        
        return success_response(message='会话删除成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'删除会话异常: {str(e)}', exc_info=True)
        return error_response(500, '删除会话失败')


@chat_bp.route('/session/rename', methods=['POST'])
@require_auth
def rename_session():
    """
    重命名会话
    POST /api/chat/session/rename
    """
    try:
        from flask import g
        data = request.get_json()
        
        session_id = data.get('sessionId')
        title = data.get('title', '').strip()
        
        if not session_id or not title:
            return error_response(3001, '会话ID和标题不能为空')
        
        # 查询会话
        session = ChatSession.query.get(session_id)
        if not session:
            return error_response(3003, '会话不存在')
        
        # 权限检查
        if session.user_id != g.user_id:
            return error_response(403, '无权限修改该会话')
        
        # 更新标题
        session.title = title
        session.updated_at = get_beijing_now()
        
        db.session.commit()
        
        current_app.logger.info(f'重命名会话: {session_id} -> {title}')
        
        return success_response(message='会话重命名成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'重命名会话异常: {str(e)}', exc_info=True)
        return error_response(500, '重命名会话失败')

