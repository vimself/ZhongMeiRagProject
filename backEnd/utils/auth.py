"""
认证相关工具函数
"""
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, current_app, g
from utils.response import error_response


def generate_token(user_id, expiration_hours=None):
    """
    生成JWT token
    
    Args:
        user_id: 用户ID
        expiration_hours: 过期时间（小时），默认从配置读取
    
    Returns:
        str: JWT token
    """
    if expiration_hours is None:
        expiration_hours = current_app.config['JWT_EXPIRATION_HOURS']
    
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=expiration_hours),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm=current_app.config['JWT_ALGORITHM']
    )
    
    return token


def verify_token(token):
    """
    验证JWT token
    
    Args:
        token: JWT token字符串
    
    Returns:
        dict: payload数据，包含user_id
        None: token无效
    """
    try:
        # 移除 "Bearer " 前缀
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=[current_app.config['JWT_ALGORITHM']]
        )
        return payload
    except jwt.ExpiredSignatureError:
        current_app.logger.warning('Token已过期')
        return None
    except jwt.InvalidTokenError as e:
        current_app.logger.warning(f'无效的token: {str(e)}')
        return None


def require_auth(f):
    """
    需要登录的装饰器
    验证请求头中的Authorization token
    将用户ID存储在g.user_id中
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 获取Authorization头
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            current_app.logger.warning('缺少Authorization头')
            return error_response(401, '请先登录')
        
        # 验证token
        payload = verify_token(auth_header)
        if not payload:
            return error_response(401, '登录已过期，请重新登录')
        
        # 存储用户ID到g对象
        g.user_id = payload['user_id']
        g.token_payload = payload
        
        # 查询用户信息（可选）
        from models.user import User
        user = User.query.get(g.user_id)
        if not user:
            return error_response(401, '用户不存在')
        
        if not user.is_active():
            return error_response(403, '账号已被禁用')
        
        g.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_admin(f):
    """
    需要管理员权限的装饰器
    在require_auth基础上验证管理员角色
    """
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        if not g.current_user.is_admin():
            current_app.logger.warning(f'用户 {g.user_id} 尝试访问管理员接口')
            return error_response(403, '权限不足，需要管理员权限')
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_current_user_id():
    """获取当前登录用户ID"""
    return getattr(g, 'user_id', None)


def get_current_user():
    """获取当前登录用户对象"""
    return getattr(g, 'current_user', None)

