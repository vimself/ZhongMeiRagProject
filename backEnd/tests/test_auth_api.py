"""
认证API测试
测试登录、登出、修改密码等功能
"""
import pytest
from models.user import User


@pytest.mark.api
@pytest.mark.auth
class TestAuthAPI:
    """认证API测试类"""
    
    def test_login_success(self, client, db_session, admin_user):
        """测试登录成功"""
        # Arrange
        data = {
            'username': 'admin',
            'password': 'Admin123!'
        }
        
        # Act
        response = client.post('/api/auth/login', json=data)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'token' in json_data['body']
        assert 'user' in json_data['body']
        assert json_data['body']['user']['username'] == 'admin'
    
    def test_login_invalid_username(self, client, db_session):
        """测试用户名错误"""
        # Arrange
        data = {
            'username': 'nonexistent',
            'password': 'password'
        }
        
        # Act
        response = client.post('/api/auth/login', json=data)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1002
        assert '用户名或密码错误' in json_data['message']
    
    def test_login_invalid_password(self, client, db_session, admin_user):
        """测试密码错误"""
        # Arrange
        data = {
            'username': 'admin',
            'password': 'wrongpassword'
        }
        
        # Act
        response = client.post('/api/auth/login', json=data)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1002
    
    def test_login_disabled_user(self, client, db_session, disabled_user):
        """测试禁用用户登录"""
        # Arrange
        data = {
            'username': 'disabled',
            'password': 'Disabled123!'
        }
        
        # Act
        response = client.post('/api/auth/login', json=data)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1003
        assert '禁用' in json_data['message']
    
    def test_login_missing_fields(self, client, db_session):
        """测试缺少必填字段"""
        # Arrange
        data = {
            'username': 'admin'
            # 缺少password
        }
        
        # Act
        response = client.post('/api/auth/login', json=data)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1001
    
    def test_logout_success(self, client, db_session, auth_headers_user):
        """测试登出成功"""
        # Act
        response = client.post('/api/auth/logout', headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert '登出成功' in json_data['message']
    
    def test_logout_without_token(self, client, db_session):
        """测试未登录状态登出"""
        # Act
        response = client.post('/api/auth/logout')
        
        # Assert
        assert response.status_code == 401
    
    def test_change_password_success(self, client, db_session, auth_headers_user):
        """测试修改密码成功"""
        # Arrange
        data = {
            'oldPassword': 'Test123!',
            'newPassword': 'NewPass123!'
        }
        
        # Act
        response = client.post('/api/auth/change-password', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert '修改成功' in json_data['message']
    
    def test_change_password_wrong_old_password(self, client, db_session, auth_headers_user):
        """测试原密码错误"""
        # Arrange
        data = {
            'oldPassword': 'WrongOldPass!',
            'newPassword': 'NewPass123!'
        }
        
        # Act
        response = client.post('/api/auth/change-password', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1004
    
    def test_change_password_weak_password(self, client, db_session, auth_headers_user):
        """测试弱密码"""
        # Arrange
        data = {
            'oldPassword': 'Test123!',
            'newPassword': '123'  # 太弱的密码
        }
        
        # Act
        response = client.post('/api/auth/change-password', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1001
    
    def test_reset_password_not_implemented(self, client, db_session):
        """测试重置密码（未实现）"""
        # Arrange
        data = {
            'account': 'test@example.com',
            'code': '123456',
            'newPassword': 'NewPass123!'
        }
        
        # Act
        response = client.post('/api/auth/reset-password', json=data)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1005


