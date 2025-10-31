"""
管理员用户管理API测试
测试用户CRUD、状态管理等功能
"""
import pytest
from models.user import User


@pytest.mark.api
@pytest.mark.admin
class TestAdminUsersAPI:
    """管理员用户管理API测试类"""
    
    def test_get_stats(self, client, db_session, auth_headers_admin, admin_user, normal_user):
        """测试获取用户统计"""
        # Act
        response = client.post('/api/admin/users/stats', headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'totalUsers' in json_data['body']
        assert 'activeUsers' in json_data['body']
        assert 'adminUsers' in json_data['body']
        assert json_data['body']['totalUsers'] >= 2
    
    def test_get_list(self, client, db_session, auth_headers_admin, admin_user, normal_user):
        """测试获取用户列表"""
        # Arrange
        data = {
            'page': 1,
            'pageSize': 10
        }
        
        # Act
        response = client.post('/api/admin/users/list', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'list' in json_data['body']
        assert 'total' in json_data['body']
        assert json_data['body']['total'] >= 2
    
    def test_get_list_with_filters(self, client, db_session, auth_headers_admin, admin_user):
        """测试带过滤条件的用户列表"""
        # Arrange
        data = {
            'keyword': 'admin',
            'role': 'admin',
            'status': 'active',
            'page': 1,
            'pageSize': 10
        }
        
        # Act
        response = client.post('/api/admin/users/list', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['total'] >= 1
    
    def test_create_user(self, client, db_session, auth_headers_admin):
        """测试创建用户"""
        # Arrange
        data = {
            'username': 'newuser',
            'password': 'NewUser123!',
            'name': '新用户',
            'email': 'newuser@example.com',
            'phone': '13900139001',
            'role': 'user'
        }
        
        # Act
        response = client.post('/api/admin/users/create', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['username'] == 'newuser'
    
    def test_create_user_duplicate_username(self, client, db_session, auth_headers_admin, normal_user):
        """测试创建重复用户名"""
        # Arrange
        data = {
            'username': 'testuser',  # 已存在
            'password': 'Test123!',
            'name': '测试',
            'email': 'test2@example.com'
        }
        
        # Act
        response = client.post('/api/admin/users/create', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1003
    
    def test_create_user_invalid_email(self, client, db_session, auth_headers_admin):
        """测试无效邮箱"""
        # Arrange
        data = {
            'username': 'newuser',
            'password': 'Test123!',
            'name': '测试',
            'email': 'invalid-email'
        }
        
        # Act
        response = client.post('/api/admin/users/create', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1001
    
    def test_update_user(self, client, db_session, auth_headers_admin, normal_user):
        """测试更新用户"""
        # Arrange
        data = {
            'id': normal_user.id,
            'name': '更新的名字',
            'email': 'updated@example.com'
        }
        
        # Act
        response = client.post('/api/admin/users/update', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['name'] == '更新的名字'
    
    def test_delete_user(self, client, db_session, auth_headers_admin, normal_user):
        """测试删除用户"""
        # Arrange
        data = {
            'userId': normal_user.id
        }
        
        # Act
        response = client.post('/api/admin/users/delete', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        
        # 验证已删除
        user = User.query.get(normal_user.id)
        assert user is None
    
    def test_delete_self(self, client, db_session, auth_headers_admin, admin_user):
        """测试删除自己"""
        # Arrange
        data = {
            'userId': admin_user.id
        }
        
        # Act
        response = client.post('/api/admin/users/delete', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1005
    
    def test_toggle_status(self, client, db_session, auth_headers_admin, normal_user):
        """测试切换用户状态"""
        # Arrange
        data = {
            'userId': normal_user.id,
            'status': 'disabled'
        }
        
        # Act
        response = client.post('/api/admin/users/toggle-status', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        
        # 验证状态已更新
        user = User.query.get(normal_user.id)
        assert user.status == 'disabled'
    
    def test_reset_password(self, client, db_session, auth_headers_admin, normal_user):
        """测试重置密码"""
        # Arrange
        data = {
            'userId': normal_user.id
        }
        
        # Act
        response = client.post('/api/admin/users/reset-password', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'newPassword' in json_data['body']
    
    def test_export_users_not_implemented(self, client, db_session, auth_headers_admin):
        """测试导出用户（未实现）"""
        # Act
        response = client.post('/api/admin/users/export', headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 1006


