"""
模型管理模块API（管理员）
包含模型CRUD、健康检查等接口
"""
from flask import Blueprint, request, current_app
from models.model import Model
from utils.auth import require_admin
from utils.response import success_response, error_response
from utils.helpers import generate_id, paginate
from app import db
from datetime import datetime
import requests

models_bp = Blueprint('models_api', __name__)


@models_bp.route('/stats', methods=['GET', 'POST'])
@require_admin
def get_stats():
    """
    获取模型统计
    GET/POST /api/models/stats
    """
    try:
        llm_count = Model.query.filter_by(type='llm').count()
        embedding_count = Model.query.filter_by(type='embedding').count()
        online_count = Model.query.filter_by(status='online').count()
        offline_count = Model.query.filter(
            Model.status.in_(['offline', 'error'])
        ).count()
        
        stats = {
            'llmCount': llm_count,
            'embeddingCount': embedding_count,
            'onlineCount': online_count,
            'offlineCount': offline_count
        }
        
        return success_response(stats)
        
    except Exception as e:
        current_app.logger.error(f'获取模型统计异常: {str(e)}', exc_info=True)
        return error_response(500, '获取模型统计失败')


@models_bp.route('/list', methods=['POST'])
@require_admin
def get_list():
    """
    获取模型列表
    POST /api/models/list
    """
    try:
        data = request.get_json() or {}
        
        # 获取参数
        model_type = data.get('type', 'all')
        status = data.get('status', 'all')
        page = int(data.get('page', 1))
        page_size = int(data.get('pageSize', 20))
        
        # 构建查询
        query = Model.query
        
        # 类型过滤
        if model_type and model_type != 'all':
            query = query.filter_by(type=model_type)
        
        # 状态过滤
        if status and status != 'all':
            query = query.filter_by(status=status)
        
        # 排序
        query = query.order_by(Model.created_at.desc())
        
        # 分页
        result = paginate(query, page, page_size)
        
        # 添加延迟字符串
        for model in result['list']:
            model['latency'] = get_latency_str(model.get('responseTime'))
        
        return success_response(result)
        
    except Exception as e:
        current_app.logger.error(f'获取模型列表异常: {str(e)}', exc_info=True)
        return error_response(500, '获取模型列表失败')


@models_bp.route('/detail', methods=['POST'])
@require_admin
def get_detail():
    """
    获取模型详情
    POST /api/models/detail
    """
    try:
        data = request.get_json()
        
        model_id = data.get('id')
        if not model_id:
            return error_response(5001, '模型ID不能为空')
        
        model = Model.query.get(model_id)
        if not model:
            return error_response(5002, '模型不存在')
        
        return success_response(model.to_dict())
        
    except Exception as e:
        current_app.logger.error(f'获取模型详情异常: {str(e)}', exc_info=True)
        return error_response(500, '获取模型详情失败')


@models_bp.route('/create', methods=['POST'])
@require_admin
def create_model():
    """
    创建模型
    POST /api/models/create
    """
    try:
        data = request.get_json()
        
        # 获取参数
        name = data.get('name', '').strip()
        model_type = data.get('type')
        description = data.get('description', '').strip()
        provider = data.get('provider', '').strip()
        endpoint = data.get('endpoint', '').strip()
        
        # 参数验证
        if not name or not model_type:
            return error_response(5001, '模型名称和类型不能为空')
        
        if model_type not in ['llm', 'embedding']:
            return error_response(5001, '模型类型必须是llm或embedding')
        
        # 检查名称是否已存在
        existing = Model.query.filter_by(name=name).first()
        if existing:
            return error_response(5003, '模型名称已存在')
        
        # 创建模型
        model = Model(
            id=generate_id('model'),
            name=name,
            type=model_type,
            description=description,
            provider=provider,
            endpoint=endpoint,
            model_size=data.get('modelSize'),
            context_length=data.get('contextLength'),
            gpu_memory=data.get('gpuMemory'),
            config=data.get('config', {}),
            status='offline',
            is_default=False,
            created_at=datetime.utcnow()
        )
        
        db.session.add(model)
        db.session.commit()
        
        current_app.logger.info(f'创建模型: {name}')
        
        # 自动执行健康检查
        check_model_health(model)
        
        return success_response(model.to_dict(), '模型创建成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'创建模型异常: {str(e)}', exc_info=True)
        return error_response(500, '创建模型失败')


@models_bp.route('/update', methods=['POST'])
@require_admin
def update_model():
    """
    更新模型
    POST /api/models/update
    """
    try:
        data = request.get_json()
        
        model_id = data.get('id')
        if not model_id:
            return error_response(5001, '模型ID不能为空')
        
        model = Model.query.get(model_id)
        if not model:
            return error_response(5002, '模型不存在')
        
        # 更新字段
        if 'name' in data:
            # 检查名称是否已被其他模型使用
            existing = Model.query.filter_by(name=data['name']).first()
            if existing and existing.id != model_id:
                return error_response(5003, '模型名称已存在')
            model.name = data['name'].strip()
        
        if 'description' in data:
            model.description = data['description'].strip()
        if 'endpoint' in data:
            model.endpoint = data['endpoint'].strip()
        if 'config' in data:
            if model.config:
                model.config.update(data['config'])
            else:
                model.config = data['config']
        
        model.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        current_app.logger.info(f'更新模型: {model.name}')
        
        # 自动执行健康检查
        check_model_health(model)
        
        return success_response(model.to_dict(), '模型更新成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'更新模型异常: {str(e)}', exc_info=True)
        return error_response(500, '更新模型失败')


@models_bp.route('/delete', methods=['POST'])
@require_admin
def delete_model():
    """
    删除模型
    POST /api/models/delete
    """
    try:
        data = request.get_json()
        
        model_id = data.get('id')
        if not model_id:
            return error_response(5001, '模型ID不能为空')
        
        model = Model.query.get(model_id)
        if not model:
            return error_response(5002, '模型不存在')
        
        # 不能删除默认模型
        if model.is_default:
            return error_response(5004, '不能删除默认模型')
        
        # TODO: 检查是否有知识库正在使用该模型
        
        model_name = model.name
        
        db.session.delete(model)
        db.session.commit()
        
        current_app.logger.info(f'删除模型: {model_name}')
        
        return success_response(message='模型删除成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'删除模型异常: {str(e)}', exc_info=True)
        return error_response(500, '删除模型失败')


@models_bp.route('/set-default', methods=['POST'])
@require_admin
def set_default():
    """
    设置默认模型
    POST /api/models/set-default
    """
    try:
        data = request.get_json()
        
        model_id = data.get('id')
        model_type = data.get('type')
        
        if not model_id or not model_type:
            return error_response(5001, '模型ID和类型不能为空')
        
        model = Model.query.get(model_id)
        if not model:
            return error_response(5002, '模型不存在')
        
        if model.type != model_type:
            return error_response(5001, '模型类型不匹配')
        
        # 离线状态不能设为默认
        if model.status != 'online':
            return error_response(5005, '只有在线状态的模型才能设为默认')
        
        # 取消同类型其他模型的默认状态
        Model.query.filter_by(type=model_type, is_default=True)\
            .update({'is_default': False})
        
        # 设置新的默认模型
        model.is_default = True
        model.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        current_app.logger.info(f'设置默认模型: {model.name}')
        
        return success_response(message='默认模型设置成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'设置默认模型异常: {str(e)}', exc_info=True)
        return error_response(500, '设置默认模型失败')


@models_bp.route('/test', methods=['POST'])
@require_admin
def test_model():
    """
    测试模型连接
    POST /api/models/test
    """
    try:
        data = request.get_json()
        
        model_id = data.get('id')
        if not model_id:
            return error_response(5001, '模型ID不能为空')
        
        model = Model.query.get(model_id)
        if not model:
            return error_response(5002, '模型不存在')
        
        # 执行健康检查
        result = check_model_health(model)
        
        return success_response(result)
        
    except Exception as e:
        current_app.logger.error(f'测试模型连接异常: {str(e)}', exc_info=True)
        return error_response(500, '测试模型连接失败')


@models_bp.route('/health-check', methods=['POST'])
@require_admin
def health_check():
    """
    批量健康检查
    POST /api/models/health-check
    """
    try:
        models = Model.query.all()
        
        results = []
        success_count = 0
        failed_count = 0
        
        for model in models:
            result = check_model_health(model)
            results.append({
                'id': model.id,
                'name': model.name,
                'status': result['status'],
                'responseTime': result['responseTime'],
                'message': result['message']
            })
            
            if result['status'] == 'online':
                success_count += 1
            else:
                failed_count += 1
        
        return success_response({
            'total': len(models),
            'success': success_count,
            'failed': failed_count,
            'results': results
        })
        
    except Exception as e:
        current_app.logger.error(f'批量健康检查异常: {str(e)}', exc_info=True)
        return error_response(500, '批量健康检查失败')


@models_bp.route('/update-status', methods=['POST'])
@require_admin
def update_status():
    """
    更新模型状态
    POST /api/models/update-status
    """
    try:
        data = request.get_json()
        
        model_id = data.get('id')
        status = data.get('status')
        
        if not model_id or not status:
            return error_response(5001, '模型ID和状态不能为空')
        
        if status not in ['online', 'offline']:
            return error_response(5001, '状态值不正确')
        
        model = Model.query.get(model_id)
        if not model:
            return error_response(5002, '模型不存在')
        
        model.status = status
        model.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        current_app.logger.info(f'更新模型状态: {model.name} -> {status}')
        
        return success_response(message='模型状态更新成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'更新模型状态异常: {str(e)}', exc_info=True)
        return error_response(500, '更新模型状态失败')


# 辅助函数
def check_model_health(model):
    """检查模型健康状态"""
    try:
        if not model.endpoint or model.endpoint == 'local':
            # 本地模型，暂时无法检查
            model.status = 'offline'
            model.last_check_time = datetime.utcnow()
            model.health_message = '本地模型，无法自动检查'
            db.session.commit()
            
            return {
                'status': 'offline',
                'responseTime': None,
                'message': '本地模型，无法自动检查',
                'timestamp': datetime.utcnow().isoformat()
            }
        
        # TODO: 实现真实的健康检查
        # 对于LLM模型：调用API测试接口
        # 对于Embedding模型：测试向量化功能
        
        model.status = 'offline'
        model.last_check_time = datetime.utcnow()
        model.health_message = '健康检查功能开发中'
        db.session.commit()
        
        return {
            'status': 'offline',
            'responseTime': None,
            'message': '健康检查功能开发中',
            'timestamp': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        current_app.logger.error(f'健康检查异常: {str(e)}')
        
        model.status = 'error'
        model.last_check_time = datetime.utcnow()
        model.health_message = str(e)
        db.session.commit()
        
        return {
            'status': 'error',
            'responseTime': None,
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }


def get_latency_str(response_time):
    """获取延迟字符串"""
    if response_time is None:
        return '-'
    return f'{response_time}ms'

