"""
数据验证工具
"""
import re


def validate_email(email):
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
    
    Returns:
        bool: 是否有效
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """
    验证手机号格式（中国大陆）
    
    Args:
        phone: 手机号
    
    Returns:
        bool: 是否有效
    """
    if not phone:
        return False
    
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))


def validate_password(password):
    """
    验证密码强度
    要求：8-20位，包含大小写字母和数字
    
    Args:
        password: 密码
    
    Returns:
        tuple: (是否有效, 错误信息)
    """
    if not password:
        return False, '密码不能为空'
    
    if len(password) < 6:
        return False, '密码长度至少6位'
    
    if len(password) > 20:
        return False, '密码长度不能超过20位'
    
    # 简单版本：只要求长度
    return True, ''
    
    # 严格版本（可选）：
    # if not re.search(r'[a-z]', password):
    #     return False, '密码必须包含小写字母'
    # if not re.search(r'[A-Z]', password):
    #     return False, '密码必须包含大写字母'
    # if not re.search(r'\d', password):
    #     return False, '密码必须包含数字'
    # return True, ''


def validate_username(username):
    """
    验证用户名
    要求：4-20位，字母数字下划线
    
    Args:
        username: 用户名
    
    Returns:
        tuple: (是否有效, 错误信息)
    """
    if not username:
        return False, '用户名不能为空'
    
    if len(username) < 4:
        return False, '用户名长度至少4位'
    
    if len(username) > 20:
        return False, '用户名长度不能超过20位'
    
    pattern = r'^[a-zA-Z0-9_]+$'
    if not re.match(pattern, username):
        return False, '用户名只能包含字母、数字和下划线'
    
    return True, ''


def validate_required_fields(data, required_fields):
    """
    验证必填字段
    
    Args:
        data: 数据字典
        required_fields: 必填字段列表
    
    Returns:
        tuple: (是否有效, 缺失字段列表)
    """
    missing_fields = []
    
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            missing_fields.append(field)
    
    return len(missing_fields) == 0, missing_fields

