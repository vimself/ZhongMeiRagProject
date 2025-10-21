"""
统一响应格式工具
"""
from flask import jsonify


def success_response(data=None, message='操作成功', status_code=200):
    """
    成功响应
    
    Args:
        data: 业务数据
        message: 提示信息
        status_code: HTTP状态码
    
    Returns:
        Flask Response对象
    """
    response = {
        'error': 0,
        'message': message,
        'body': data if data is not None else {}
    }
    return jsonify(response), status_code


def error_response(error_code, message='操作失败', data=None, status_code=None):
    """
    错误响应
    
    Args:
        error_code: 错误码
        message: 错误信息
        data: 额外数据
        status_code: HTTP状态码，不传则根据error_code自动判断
    
    Returns:
        Flask Response对象
    """
    # 如果未指定HTTP状态码，根据错误码判断
    if status_code is None:
        if error_code == 401:
            status_code = 401
        elif error_code == 403:
            status_code = 403
        elif error_code == 404:
            status_code = 404
        elif error_code == 500:
            status_code = 500
        else:
            status_code = 400
    
    response = {
        'error': error_code,
        'message': message,
        'body': data if data is not None else {}
    }
    return jsonify(response), status_code

