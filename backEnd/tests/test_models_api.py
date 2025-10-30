"""
模型管理API测试
测试模型CRUD、健康检查等功能
"""
import pytest
from models.model import Model


@pytest.mark.api
@pytest.mark.admin
class TestModelsAPI:
    """模型管理API测试类"""
    
    def test_get_stats(self, client, db_session, auth_headers_admin, llm_model, embedding_model):
        """测试获取模型统计"""
        # Act
        response = client.post('/api/models/stats', headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'llmCount' in json_data['body']
        assert 'embeddingCount' in json_data['body']
        assert json_data['body']['llmCount'] >= 1
        assert json_data['body']['embeddingCount'] >= 1
    
    def test_get_list(self, client, db_session, auth_headers_admin, llm_model, embedding_model):
        """测试获取模型列表"""
        # Arrange
        data = {
            'type': 'all',
            'status': 'all',
            'page': 1,
            'pageSize': 20
        }
        
        # Act
        response = client.post('/api/models/list', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'list' in json_data['body']
        assert json_data['body']['total'] >= 2
    
    def test_get_list_filter_by_type(self, client, db_session, auth_headers_admin, llm_model):
        """测试按类型过滤模型"""
        # Arrange
        data = {
            'type': 'llm',
            'page': 1,
            'pageSize': 20
        }
        
        # Act
        response = client.post('/api/models/list', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['total'] >= 1
    
    def test_get_detail(self, client, db_session, auth_headers_admin, llm_model):
        """测试获取模型详情"""
        # Arrange
        data = {
            'id': llm_model.id
        }
        
        # Act
        response = client.post('/api/models/detail', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['id'] == llm_model.id
    
    def test_create_model(self, client, db_session, auth_headers_admin):
        """测试创建模型"""
        # Arrange
        data = {
            'name': '新模型',
            'type': 'llm',
            'description': '测试模型',
            'provider': 'openai',
            'endpoint': 'http://localhost:8001/v1'
        }
        
        # Act
        response = client.post('/api/models/create', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['name'] == '新模型'
    
    def test_create_model_duplicate_name(self, client, db_session, auth_headers_admin, llm_model):
        """测试创建重名模型"""
        # Arrange
        data = {
            'name': '测试LLM模型',  # 已存在
            'type': 'llm',
            'description': '测试',
            'provider': 'openai'
        }
        
        # Act
        response = client.post('/api/models/create', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 5003
    
    def test_create_model_invalid_type(self, client, db_session, auth_headers_admin):
        """测试无效模型类型"""
        # Arrange
        data = {
            'name': '测试',
            'type': 'invalid_type',
            'description': '测试'
        }
        
        # Act
        response = client.post('/api/models/create', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 5001
    
    def test_update_model(self, client, db_session, auth_headers_admin, llm_model):
        """测试更新模型"""
        # Arrange
        data = {
            'id': llm_model.id,
            'name': '更新的模型名',
            'description': '更新的描述'
        }
        
        # Act
        response = client.post('/api/models/update', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['name'] == '更新的模型名'
    
    def test_delete_model(self, client, db_session, auth_headers_admin, llm_model):
        """测试删除模型"""
        # 先取消默认状态
        llm_model.is_default = False
        db_session.session.commit()
        
        # Arrange
        data = {
            'id': llm_model.id
        }
        
        # Act
        response = client.post('/api/models/delete', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
    
    def test_delete_default_model(self, client, db_session, auth_headers_admin, llm_model):
        """测试删除默认模型"""
        # Arrange
        data = {
            'id': llm_model.id
        }
        
        # Act
        response = client.post('/api/models/delete', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 5004
    
    def test_set_default(self, client, db_session, auth_headers_admin, llm_model):
        """测试设置默认模型"""
        # Arrange
        data = {
            'id': llm_model.id,
            'type': 'llm'
        }
        
        # Act
        response = client.post('/api/models/set-default', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
    
    def test_test_model(self, client, db_session, auth_headers_admin, llm_model):
        """测试模型连接"""
        # Arrange
        data = {
            'id': llm_model.id
        }
        
        # Act
        response = client.post('/api/models/test', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'status' in json_data['body']
    
    def test_health_check(self, client, db_session, auth_headers_admin, llm_model):
        """测试批量健康检查"""
        # Act
        response = client.post('/api/models/health-check', headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'total' in json_data['body']
        assert 'results' in json_data['body']
    
    def test_update_status(self, client, db_session, auth_headers_admin, llm_model):
        """测试更新模型状态"""
        # Arrange
        data = {
            'id': llm_model.id,
            'status': 'offline'
        }
        
        # Act
        response = client.post('/api/models/update-status', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0

