"""
用户认证模块API
包含登录、登出、修改密码、重置密码等接口
"""
from flask import Blueprint, request, current_app
from datetime import datetime

from extensions import db
from models.user import User
from models.login_record import LoginRecord
from utils.auth import generate_token, require_auth
from utils.response import success_response, error_response
from utils.helpers import hash_password, verify_password, generate_id, get_client_ip, parse_device_info, get_beijing_now
from utils.validators import validate_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    POST /api/auth/login
    """
    try:
        data = request.get_json()
        
        # 获取参数
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # 参数验证
        if not username or not password:
            return error_response(1001, '用户名和密码不能为空')
        
        # 查询用户
        user = User.query.filter_by(username=username).first()
        
        # 验证用户和密码
        if not user:
            current_app.logger.warning(f'登录失败: 用户不存在 - {username}')
            return error_response(1002, '用户名或密码错误')
        
        if not verify_password(password, user.password_hash):
            current_app.logger.warning(f'登录失败: 密码错误 - {username}')
            return error_response(1002, '用户名或密码错误')
        
        # 检查用户状态
        if not user.is_active():
            current_app.logger.warning(f'登录失败: 账号已禁用 - {username}')
            return error_response(1003, '账号已被禁用，请联系管理员')
        
        # 生成token
        token = generate_token(user.id)
        
        # 更新最后登录时间
        user.last_login_at = get_beijing_now()
        
        # 获取登录信息
        client_ip = get_client_ip(request)
        device = parse_device_info(request.headers.get('User-Agent'))
        user_agent = request.headers.get('User-Agent')
        
        # 查找相同设备和IP的登录记录
        existing_record = LoginRecord.query.filter_by(
            user_id=user.id,
            ip=client_ip,
            device=device
        ).first()
        
        if existing_record:
            # 更新现有记录
            existing_record.last_login_time = get_beijing_now()
            existing_record.login_count = (existing_record.login_count or 1) + 1
            existing_record.status = 'current'
            existing_record.user_agent = user_agent
            current_app.logger.info(f'更新登录记录: {user.username}, 登录次数: {existing_record.login_count}')
        else:
            # 创建新的登录记录
            login_record = LoginRecord(
                id=generate_id('login'),
                user_id=user.id,
                ip=client_ip,
                device=device,
                user_agent=user_agent,
                status='current',
                login_time=get_beijing_now(),
                last_login_time=get_beijing_now(),
                login_count=1
            )
            db.session.add(login_record)
            current_app.logger.info(f'创建新登录记录: {user.username}')
        
        db.session.commit()
        
        current_app.logger.info(f'用户登录成功: {username}')
        
        # 返回token和用户信息
        return success_response({
            'token': token,
            'user': user.to_dict()
        }, '登录成功')
        
    except Exception as e:
        current_app.logger.error(f'登录异常: {str(e)}', exc_info=True)
        return error_response(500, '登录失败，请稍后重试')


@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """
    用户登出
    POST /api/auth/logout
    """
    try:
        from flask import g
        
        # 更新登录记录为已结束
        login_record = LoginRecord.query.filter_by(
            user_id=g.user_id,
            status='current'
        ).first()
        
        if login_record:
            login_record.status = 'ended'
            login_record.logout_time = get_beijing_now()
            db.session.commit()
        
        current_app.logger.info(f'用户登出: {g.user_id}')
        
        return success_response(message='登出成功')
        
    except Exception as e:
        current_app.logger.error(f'登出异常: {str(e)}', exc_info=True)
        return error_response(500, '登出失败，请稍后重试')


@auth_bp.route('/change-password', methods=['POST'])
@require_auth
def change_password():
    """
    修改密码
    POST /api/auth/change-password
    """
    try:
        from flask import g
        data = request.get_json()
        
        # 获取参数
        old_password = data.get('oldPassword', '')
        new_password = data.get('newPassword', '')
        
        # 参数验证
        if not old_password or not new_password:
            return error_response(1001, '原密码和新密码不能为空')
        
        # 验证密码强度
        is_valid, error_msg = validate_password(new_password)
        if not is_valid:
            return error_response(1001, error_msg)
        
        # 查询用户
        user = User.query.get(g.user_id)
        if not user:
            return error_response(401, '用户不存在')
        
        # 验证原密码
        if not verify_password(old_password, user.password_hash):
            current_app.logger.warning(f'修改密码失败: 原密码错误 - {user.username}')
            return error_response(1004, '原密码错误')
        
        # 更新密码
        user.password_hash = hash_password(new_password)
        user.updated_at = get_beijing_now()
        
        db.session.commit()
        
        current_app.logger.info(f'用户修改密码成功: {user.username}')
        
        return success_response(message='密码修改成功，请重新登录')
        
    except Exception as e:
        current_app.logger.error(f'修改密码异常: {str(e)}', exc_info=True)
        return error_response(500, '修改密码失败，请稍后重试')


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    重置密码（通过验证码）
    POST /api/auth/reset-password
    """
    try:
        data = request.get_json()
        
        # 获取参数
        account = data.get('account', '').strip()
        code = data.get('code', '')
        new_password = data.get('newPassword', '')
        
        # 参数验证
        if not account or not code or not new_password:
            return error_response(1001, '账号、验证码和新密码不能为空')
        
        # 验证密码强度
        is_valid, error_msg = validate_password(new_password)
        if not is_valid:
            return error_response(1001, error_msg)
        
        # TODO: 验证验证码（需要实现短信/邮件验证码功能）
        # 暂时返回未实现
        return error_response(1005, '密码重置功能暂未开放，请联系管理员')
        
    except Exception as e:
        current_app.logger.error(f'重置密码异常: {str(e)}', exc_info=True)
        return error_response(500, '重置密码失败，请稍后重试')

