"""
用户个人中心API测试
测试个人信息、登录记录等功能
"""
import pytest


@pytest.mark.api
class TestUserAPI:
    """用户API测试类"""
    
    def test_get_profile_success(self, client, db_session, auth_headers_user, normal_user):
        """测试获取个人信息"""
        # Act
        response = client.post('/api/user/profile', headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['username'] == 'testuser'
        assert json_data['body']['name'] == '测试用户'
    
    def test_get_profile_without_auth(self, client, db_session):
        """测试未登录获取个人信息"""
        # Act
        response = client.post('/api/user/profile')
        
        # Assert
        assert response.status_code == 401
    
    def test_update_profile_success(self, client, db_session, auth_headers_user):
        """测试更新个人信息"""
        # Arrange
        data = {
            'name': '更新的姓名',
            'email': 'updated@example.com',
            'phone': '13800138001',
            'department': 'tech',
            'position': '工程师',
            'bio': '这是我的简介'
        }
        
        # Act
        response = client.post('/api/user/profile/update', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['name'] == '更新的姓名'
        assert json_data['body']['email'] == 'updated@example.com'
    
    def test_update_profile_invalid_email(self, client, db_session, auth_headers_user):
        """测试无效邮箱格式"""
        # Arrange
        data = {
            'name': '测试',
            'email': 'invalid-email'
        }
        
        # Act
        response = client.post('/api/user/profile/update', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1001
        assert '邮箱' in json_data['message']
    
    def test_update_profile_invalid_phone(self, client, db_session, auth_headers_user):
        """测试无效手机号格式"""
        # Arrange
        data = {
            'name': '测试',
            'email': 'test@example.com',
            'phone': '123'  # 无效手机号
        }
        
        # Act
        response = client.post('/api/user/profile/update', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1001
        assert '手机号' in json_data['message']
    
    def test_update_profile_bio_too_long(self, client, db_session, auth_headers_user):
        """测试简介过长"""
        # Arrange
        data = {
            'name': '测试',
            'email': 'test@example.com',
            'bio': 'a' * 201  # 超过200字符
        }
        
        # Act
        response = client.post('/api/user/profile/update', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1001
        assert '简介' in json_data['message']
    
    def test_get_departments(self, client, db_session, auth_headers_user):
        """测试获取部门列表"""
        # Act
        response = client.post('/api/user/departments', headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert isinstance(json_data['body'], list)
        assert len(json_data['body']) > 0
    
    def test_get_login_records(self, client, db_session, auth_headers_user):
        """测试获取登录记录"""
        # Act
        response = client.post('/api/user/login-records', 
                              json={'limit': 10}, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert isinstance(json_data['body'], list)
    
    def test_change_password_success(self, client, db_session, auth_headers_user):
        """测试修改密码"""
        # Arrange
        data = {
            'currentPassword': 'Test123!',
            'newPassword': 'NewPass123!',
            'confirmPassword': 'NewPass123!'
        }
        
        # Act
        response = client.post('/api/user/change-password', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
    
    def test_change_password_mismatch(self, client, db_session, auth_headers_user):
        """测试两次密码不一致"""
        # Arrange
        data = {
            'currentPassword': 'Test123!',
            'newPassword': 'NewPass123!',
            'confirmPassword': 'Different123!'
        }
        
        # Act
        response = client.post('/api/user/change-password', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1001
        assert '不一致' in json_data['message']
    
    def test_upload_avatar_not_implemented(self, client, db_session, auth_headers_user):
        """测试上传头像（未实现）"""
        # Act
        response = client.post('/api/user/avatar/upload', headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1001


