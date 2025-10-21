"""
通用辅助函数
"""
import uuid
import bcrypt
from datetime import datetime


def generate_id(prefix=''):
    """
    生成唯一ID
    
    Args:
        prefix: ID前缀
    
    Returns:
        str: 唯一ID
    """
    unique_id = str(uuid.uuid4()).replace('-', '')[:16]
    if prefix:
        return f'{prefix}_{unique_id}'
    return unique_id


def hash_password(password):
    """
    对密码进行哈希加密
    
    Args:
        password: 明文密码
    
    Returns:
        str: 加密后的密码哈希
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, password_hash):
    """
    验证密码
    
    Args:
        password: 明文密码
        password_hash: 密码哈希
    
    Returns:
        bool: 密码是否匹配
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False


def parse_device_info(user_agent):
    """
    解析User-Agent获取设备信息
    
    Args:
        user_agent: User-Agent字符串
    
    Returns:
        str: 设备类型描述
    """
    if not user_agent:
        return 'Unknown Device'
    
    user_agent = user_agent.lower()
    
    if 'mobile' in user_agent or 'android' in user_agent:
        return 'Mobile Device'
    elif 'ipad' in user_agent or 'tablet' in user_agent:
        return 'Tablet'
    elif 'windows' in user_agent:
        return 'Windows PC'
    elif 'mac' in user_agent:
        return 'Mac'
    elif 'linux' in user_agent:
        return 'Linux'
    else:
        return 'Unknown Device'


def get_client_ip(request):
    """
    获取客户端IP地址
    
    Args:
        request: Flask request对象
    
    Returns:
        str: IP地址
    """
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr


def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """
    格式化日期时间
    
    Args:
        dt: datetime对象
        format_str: 格式字符串
    
    Returns:
        str: 格式化后的日期时间字符串
    """
    if dt is None:
        return ''
    if isinstance(dt, str):
        return dt
    return dt.strftime(format_str)


def paginate(query, page, page_size, max_page_size=100):
    """
    分页查询
    
    Args:
        query: SQLAlchemy查询对象
        page: 页码（从1开始）
        page_size: 每页数量
        max_page_size: 最大每页数量
    
    Returns:
        dict: 包含list, total, page, pageSize的字典
    """
    # 参数校验
    page = max(1, int(page))
    page_size = min(max(1, int(page_size)), max_page_size)
    
    # 计算总数
    total = query.count()
    
    # 查询当前页数据
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        'list': [item.to_dict() if hasattr(item, 'to_dict') else item for item in items],
        'total': total,
        'page': page,
        'pageSize': page_size
    }

