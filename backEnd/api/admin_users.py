"""
用户管理模块API（管理员）
包含用户CRUD、状态管理等接口
"""
from flask import Blueprint, request, current_app
from models.user import User
from utils.auth import require_admin
from utils.response import success_response, error_response
from utils.helpers import generate_id, hash_password, paginate, get_beijing_now
from utils.validators import validate_email, validate_phone, validate_username, validate_password
from extensions import db
from datetime import datetime
import random
import string

admin_users_bp = Blueprint('admin_users', __name__)


@admin_users_bp.route('/stats', methods=['POST'])
@require_admin
def get_stats():
    """
    获取用户统计
    POST /api/admin/users/stats
    """
    try:
        total_users = User.query.count()
        active_users = User.query.filter_by(status='active').count()
        admin_users = User.query.filter_by(role='admin').count()
        disabled_users = User.query.filter_by(status='disabled').count()
        
        stats = {
            'totalUsers': total_users,
            'activeUsers': active_users,
            'adminUsers': admin_users,
            'disabledUsers': disabled_users
        }
        
        return success_response(stats)
        
    except Exception as e:
        current_app.logger.error(f'获取用户统计异常: {str(e)}', exc_info=True)
        return error_response(500, '获取用户统计失败')


@admin_users_bp.route('/list', methods=['POST'])
@require_admin
def get_list():
    """
    获取用户列表
    POST /api/admin/users/list
    """
    try:
        data = request.get_json() or {}
        
        # 获取参数
        keyword = data.get('keyword', '').strip()
        role = data.get('role', '')
        status = data.get('status', '')
        page = int(data.get('page', 1))
        page_size = int(data.get('pageSize', 10))
        
        # 构建查询
        query = User.query
        
        # 关键词搜索
        if keyword:
            query = query.filter(
                (User.username.like(f'%{keyword}%')) |
                (User.name.like(f'%{keyword}%')) |
                (User.email.like(f'%{keyword}%'))
            )
        
        # 角色过滤
        if role and role in ['admin', 'user']:
            query = query.filter_by(role=role)
        
        # 状态过滤
        if status and status in ['active', 'disabled']:
            query = query.filter_by(status=status)
        
        # 排序
        query = query.order_by(User.created_at.desc())
        
        # 分页
        result = paginate(query, page, page_size)
        
        # 添加头像颜色（如果没有头像）
        for user in result['list']:
            if not user.get('avatar'):
                user['avatarColor'] = generate_avatar_color()
        
        return success_response(result)
        
    except Exception as e:
        current_app.logger.error(f'获取用户列表异常: {str(e)}', exc_info=True)
        return error_response(500, '获取用户列表失败')


@admin_users_bp.route('/create', methods=['POST'])
@require_admin
def create_user():
    """
    创建用户
    POST /api/admin/users/create
    """
    try:
        data = request.get_json()
        
        # 获取参数
        username = data.get('username', '').strip()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        role = data.get('role', 'user')
        
        # 验证用户名
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            return error_response(1001, error_msg)
        
        # 验证密码
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return error_response(1001, error_msg)
        
        # 验证必填字段
        if not name or not email:
            return error_response(1001, '姓名和邮箱不能为空')
        
        # 验证邮箱
        if not validate_email(email):
            return error_response(1001, '邮箱格式不正确')
        
        # 验证手机号
        if phone and not validate_phone(phone):
            return error_response(1001, '手机号格式不正确')
        
        # 检查用户名是否已存在
        existing = User.query.filter_by(username=username).first()
        if existing:
            return error_response(1003, '用户名已存在')
        
        # 创建用户
        user = User(
            id=generate_id('user'),
            username=username,
            password_hash=hash_password(password),
            name=name,
            email=email,
            phone=phone,
            role=role,
            status='active',
            created_at=get_beijing_now()
        )
        
        db.session.add(user)
        db.session.commit()
        
        current_app.logger.info(f'创建用户: {username}')
        
        return success_response(user.to_dict(), '用户创建成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'创建用户异常: {str(e)}', exc_info=True)
        return error_response(500, '创建用户失败')


@admin_users_bp.route('/update', methods=['POST'])
@require_admin
def update_user():
    """
    更新用户
    POST /api/admin/users/update
    """
    try:
        data = request.get_json()
        
        user_id = data.get('id')
        if not user_id:
            return error_response(1001, '用户ID不能为空')
        
        user = User.query.get(user_id)
        if not user:
            return error_response(1004, '用户不存在')
        
        # 更新字段
        if 'name' in data:
            user.name = data['name'].strip()
        if 'email' in data:
            email = data['email'].strip()
            if not validate_email(email):
                return error_response(1001, '邮箱格式不正确')
            user.email = email
        if 'phone' in data:
            phone = data['phone'].strip()
            if phone and not validate_phone(phone):
                return error_response(1001, '手机号格式不正确')
            user.phone = phone
        if 'role' in data:
            user.role = data['role']
        
        user.updated_at = get_beijing_now()
        
        db.session.commit()
        
        current_app.logger.info(f'更新用户: {user.username}')
        
        return success_response(user.to_dict(), '用户更新成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'更新用户异常: {str(e)}', exc_info=True)
        return error_response(500, '更新用户失败')


@admin_users_bp.route('/delete', methods=['POST'])
@require_admin
def delete_user():
    """
    删除用户
    POST /api/admin/users/delete
    """
    try:
        from flask import g
        data = request.get_json()
        
        user_id = data.get('userId')
        if not user_id:
            return error_response(1001, '用户ID不能为空')
        
        # 不能删除自己
        if user_id == g.user_id:
            return error_response(1005, '不能删除当前登录的管理员账号')
        
        user = User.query.get(user_id)
        if not user:
            return error_response(1004, '用户不存在')
        
        username = user.username
        
        # 删除用户
        db.session.delete(user)
        db.session.commit()
        
        current_app.logger.info(f'删除用户: {username}')
        
        return success_response(message='用户删除成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'删除用户异常: {str(e)}', exc_info=True)
        return error_response(500, '删除用户失败')


@admin_users_bp.route('/toggle-status', methods=['POST'])
@require_admin
def toggle_status():
    """
    切换用户状态
    POST /api/admin/users/toggle-status
    """
    try:
        data = request.get_json()
        
        user_id = data.get('userId')
        status = data.get('status')
        
        if not user_id or not status:
            return error_response(1001, '用户ID和状态不能为空')
        
        if status not in ['active', 'disabled']:
            return error_response(1001, '状态值不正确')
        
        user = User.query.get(user_id)
        if not user:
            return error_response(1004, '用户不存在')
        
        user.status = status
        user.updated_at = get_beijing_now()
        
        db.session.commit()
        
        current_app.logger.info(f'切换用户状态: {user.username} -> {status}')
        
        return success_response(message=f'用户状态已更新为{status}')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'切换用户状态异常: {str(e)}', exc_info=True)
        return error_response(500, '切换用户状态失败')


@admin_users_bp.route('/reset-password', methods=['POST'])
@require_admin
def reset_password():
    """
    重置用户密码
    POST /api/admin/users/reset-password
    """
    try:
        data = request.get_json()
        
        user_id = data.get('userId')
        if not user_id:
            return error_response(1001, '用户ID不能为空')
        
        user = User.query.get(user_id)
        if not user:
            return error_response(1004, '用户不存在')
        
        # 生成随机密码
        new_password = generate_random_password()
        
        # 更新密码
        user.password_hash = hash_password(new_password)
        user.updated_at = get_beijing_now()
        
        db.session.commit()
        
        current_app.logger.info(f'重置用户密码: {user.username}')
        
        return success_response({
            'newPassword': new_password
        }, '密码重置成功')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'重置密码异常: {str(e)}', exc_info=True)
        return error_response(500, '重置密码失败')


@admin_users_bp.route('/export', methods=['POST'])
@require_admin
def export_users():
    """
    导出用户列表
    POST /api/admin/users/export
    """
    try:
        # TODO: 实现用户列表导出为CSV
        return error_response(1006, '导出功能开发中')
        
    except Exception as e:
        current_app.logger.error(f'导出用户列表异常: {str(e)}', exc_info=True)
        return error_response(500, '导出失败')


# 辅助函数
def generate_avatar_color():
    """生成头像颜色渐变"""
    colors = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
        'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    ]
    return random.choice(colors)


def generate_random_password(length=8):
    """生成随机密码"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

