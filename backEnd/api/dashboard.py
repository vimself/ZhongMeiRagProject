"""
仪表板模块API（管理员）
包含统计数据、系统状态等接口
"""
from flask import Blueprint, current_app
from models.user import User
from models.knowledge_base import KnowledgeBase, Document
from models.chat import ChatSession, ChatMessage
from models.model import Model
from utils.auth import require_admin
from utils.response import success_response, error_response
from datetime import datetime, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/stats', methods=['POST'])
@require_admin
def get_stats():
    """
    获取统计数据
    POST /api/dashboard/stats
    """
    try:
        # 计算今天和昨天的时间范围
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        
        # 今日提问数
        today_questions = ChatMessage.query.filter(
            ChatMessage.role == 'user',
            ChatMessage.created_at >= today_start
        ).count()
        
        yesterday_questions = ChatMessage.query.filter(
            ChatMessage.role == 'user',
            ChatMessage.created_at >= yesterday_start,
            ChatMessage.created_at < today_start
        ).count()
        
        # 计算提问数变化
        questions_change = 0
        questions_change_type = 'increase'
        if yesterday_questions > 0:
            questions_change = int((today_questions - yesterday_questions) / yesterday_questions * 100)
            if questions_change < 0:
                questions_change_type = 'decrease'
                questions_change = abs(questions_change)
        
        # 今日搜索数（使用会话数作为估算）
        today_searches = ChatSession.query.filter(
            ChatSession.created_at >= today_start
        ).count()
        
        yesterday_searches = ChatSession.query.filter(
            ChatSession.created_at >= yesterday_start,
            ChatSession.created_at < today_start
        ).count()
        
        # 计算搜索数变化
        search_change = 0
        search_change_type = 'increase'
        if yesterday_searches > 0:
            search_change = int((today_searches - yesterday_searches) / yesterday_searches * 100)
            if search_change < 0:
                search_change_type = 'decrease'
                search_change = abs(search_change)
        
        # 知识库统计
        total_kb = KnowledgeBase.query.count()
        week_ago = today_start - timedelta(days=7)
        new_kb = KnowledgeBase.query.filter(
            KnowledgeBase.created_at >= week_ago
        ).count()
        
        # 文档统计
        total_docs = Document.query.count()
        new_docs = Document.query.filter(
            Document.uploaded_at >= week_ago
        ).count()
        
        stats = {
            'todayQuestions': {
                'count': today_questions,
                'change': questions_change,
                'changeType': questions_change_type
            },
            'searchCount': {
                'count': today_searches,
                'change': search_change,
                'changeType': search_change_type
            },
            'knowledgeBaseCount': {
                'count': total_kb,
                'newCount': new_kb
            },
            'documentCount': {
                'count': total_docs,
                'newCount': new_docs
            }
        }
        
        return success_response(stats)
        
    except Exception as e:
        current_app.logger.error(f'获取统计数据异常: {str(e)}', exc_info=True)
        return error_response(500, '获取统计数据失败')


@dashboard_bp.route('/system-status', methods=['POST'])
@require_admin
def get_system_status():
    """
    获取系统状态
    POST /api/dashboard/system-status
    """
    try:
        # LLM模型状态
        llm_models = Model.query.filter_by(type='llm').all()
        llm_online = sum(1 for m in llm_models if m.status == 'online')
        llm_default = Model.query.filter_by(type='llm', is_default=True).first()
        
        # 向量模型状态
        embedding_models = Model.query.filter_by(type='embedding').all()
        embedding_online = sum(1 for m in embedding_models if m.status == 'online')
        embedding_default = Model.query.filter_by(type='embedding', is_default=True).first()
        
        # 系统状态判断
        system_status = 'normal'
        if llm_online == 0 or embedding_online == 0:
            system_status = 'error'
        elif llm_online < len(llm_models) or embedding_online < len(embedding_models):
            system_status = 'warning'
        
        status = {
            'llmModel': {
                'name': llm_default.name if llm_default else '未配置',
                'description': llm_default.description if llm_default else '',
                'status': llm_default.status if llm_default else 'offline',
                'online': llm_online,
                'total': len(llm_models)
            },
            'vectorModel': {
                'name': embedding_default.name if embedding_default else '未配置',
                'description': embedding_default.description if embedding_default else '',
                'status': embedding_default.status if embedding_default else 'offline',
                'online': embedding_online,
                'total': len(embedding_models)
            },
            'vectorDb': {
                'name': 'Chroma',
                'description': '向量数据库',
                'status': 'normal'
            },
            'relationalDb': {
                'name': 'MySQL',
                'description': '关系数据库',
                'status': 'normal'
            },
            'systemStatus': system_status,
            'lastUpdate': datetime.utcnow().isoformat()
        }
        
        return success_response(status)
        
    except Exception as e:
        current_app.logger.error(f'获取系统状态异常: {str(e)}', exc_info=True)
        return error_response(500, '获取系统状态失败')


@dashboard_bp.route('/refresh-status', methods=['POST'])
@require_admin
def refresh_status():
    """
    刷新系统状态
    POST /api/dashboard/refresh-status
    """
    try:
        # TODO: 实现真实的健康检查
        # 1. 检查LLM模型连接
        # 2. 检查向量模型
        # 3. 检查数据库连接
        # 4. 检查向量数据库
        
        # 暂时返回当前状态
        return get_system_status()
        
    except Exception as e:
        current_app.logger.error(f'刷新系统状态异常: {str(e)}', exc_info=True)
        return error_response(500, '刷新系统状态失败')

