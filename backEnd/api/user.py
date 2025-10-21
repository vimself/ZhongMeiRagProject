"""
个人中心模块API
包含获取个人信息、更新个人信息、上传头像等接口
"""
from flask import Blueprint, request, current_app
from models.user import User
from models.login_record import LoginRecord
from utils.auth import require_auth
from utils.response import success_response, error_response
from utils.helpers import hash_password, verify_password
from utils.validators import validate_email, validate_phone, validate_password
from app import db
from datetime import datetime

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['POST'])
@require_auth
def get_profile():
    """
    获取个人信息
    POST /api/user/profile
    """
    try:
        from flask import g
        
        user = User.query.get(g.user_id)
        if not user:
            return error_response(404, '用户不存在')
        
        profile = user.to_dict()
        
        return success_response(profile)
        
    except Exception as e:
        current_app.logger.error(f'获取个人信息异常: {str(e)}', exc_info=True)
        return error_response(500, '获取个人信息失败')


@user_bp.route('/profile/update', methods=['POST'])
@require_auth
def update_profile():
    """
    更新个人信息
    POST /api/user/profile/update
    """
    try:
        from flask import g
        data = request.get_json()
        
        user = User.query.get(g.user_id)
        if not user:
            return error_response(404, '用户不存在')
        
        # 获取参数
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        department = data.get('department', '').strip()
        position = data.get('position', '').strip()
        bio = data.get('bio', '').strip()
        
        # 验证必填字段
        if not name or not email:
            return error_response(1001, '姓名和邮箱不能为空')
        
        # 验证邮箱格式
        if not validate_email(email):
            return error_response(1001, '邮箱格式不正确')
        
        # 验证手机号格式（如果提供）
        if phone and not validate_phone(phone):
            return error_response(1001, '手机号格式不正确')
        
        # 验证bio长度
        if bio and len(bio) > 200:
            return error_response(1001, '个人简介最多200字符')
        
        # 更新字段
        user.name = name
        user.email = email
        user.phone = phone
        user.department = department
        user.position = position
        user.bio = bio
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        current_app.logger.info(f'用户更新个人信息: {user.username}')
        
        return success_response(user.to_dict(), '个人信息更新成功')
        
    except Exception as e:
        current_app.logger.error(f'更新个人信息异常: {str(e)}', exc_info=True)
        return error_response(500, '更新个人信息失败')


@user_bp.route('/avatar/upload', methods=['POST'])
@require_auth
def upload_avatar():
    """
    上传头像
    POST /api/user/avatar/upload
    """
    try:
        from flask import g
        
        # 检查文件
        if 'avatar' not in request.files:
            return error_response(1001, '请选择头像文件')
        
        file = request.files['avatar']
        if file.filename == '':
            return error_response(1001, '请选择头像文件')
        
        # TODO: 实现文件上传和保存逻辑
        # 1. 验证文件类型（JPG/PNG）
        # 2. 验证文件大小（≤2MB）
        # 3. 保存文件到服务器
        # 4. 更新用户头像URL
        
        return error_response(1006, '头像上传功能开发中')
        
    except Exception as e:
        current_app.logger.error(f'上传头像异常: {str(e)}', exc_info=True)
        return error_response(500, '上传头像失败')


@user_bp.route('/departments', methods=['POST'])
@require_auth
def get_departments():
    """
    获取部门列表
    POST /api/user/departments
    """
    try:
        # 返回预定义的部门列表
        departments = [
            {'value': 'tech', 'label': '技术部'},
            {'value': 'product', 'label': '产品部'},
            {'value': 'design', 'label': '设计部'},
            {'value': 'marketing', 'label': '市场部'},
            {'value': 'sales', 'label': '销售部'},
            {'value': 'hr', 'label': '人力资源部'},
            {'value': 'finance', 'label': '财务部'},
            {'value': 'admin', 'label': '行政部'}
        ]
        
        return success_response(departments)
        
    except Exception as e:
        current_app.logger.error(f'获取部门列表异常: {str(e)}', exc_info=True)
        return error_response(500, '获取部门列表失败')


@user_bp.route('/login-records', methods=['POST'])
@require_auth
def get_login_records():
    """
    获取登录记录
    POST /api/user/login-records
    """
    try:
        from flask import g
        data = request.get_json() or {}
        
        limit = int(data.get('limit', 10))
        limit = min(max(1, limit), 50)  # 限制在1-50之间
        
        # 查询登录记录
        records = LoginRecord.query.filter_by(user_id=g.user_id)\
            .order_by(LoginRecord.login_time.desc())\
            .limit(limit)\
            .all()
        
        records_data = [record.to_dict() for record in records]
        
        return success_response(records_data)
        
    except Exception as e:
        current_app.logger.error(f'获取登录记录异常: {str(e)}', exc_info=True)
        return error_response(500, '获取登录记录失败')


@user_bp.route('/change-password', methods=['POST'])
@require_auth
def change_password():
    """
    修改密码（个人中心）
    POST /api/user/change-password
    """
    try:
        from flask import g
        data = request.get_json()
        
        # 获取参数
        current_password = data.get('currentPassword', '')
        new_password = data.get('newPassword', '')
        confirm_password = data.get('confirmPassword', '')
        
        # 参数验证
        if not current_password or not new_password or not confirm_password:
            return error_response(1001, '请填写所有必填项')
        
        if new_password != confirm_password:
            return error_response(1001, '两次输入的密码不一致')
        
        # 验证密码强度
        is_valid, error_msg = validate_password(new_password)
        if not is_valid:
            return error_response(1001, error_msg)
        
        # 查询用户
        user = User.query.get(g.user_id)
        if not user:
            return error_response(404, '用户不存在')
        
        # 验证当前密码
        if not verify_password(current_password, user.password_hash):
            return error_response(1004, '当前密码错误')
        
        # 更新密码
        user.password_hash = hash_password(new_password)
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        current_app.logger.info(f'用户修改密码: {user.username}')
        
        return success_response(message='密码修改成功')
        
    except Exception as e:
        current_app.logger.error(f'修改密码异常: {str(e)}', exc_info=True)
        return error_response(500, '修改密码失败')

