"""
知识库管理API测试
测试知识库CRUD、文档管理等功能
"""
import pytest
from models.knowledge_base import KnowledgeBase


@pytest.mark.api
class TestKnowledgeBaseAPI:
    """知识库API测试类"""
    
    def test_get_stats(self, client, db_session, auth_headers_user, knowledge_base):
        """测试获取知识库统计"""
        # Act
        response = client.post('/api/knowledge-base/stats', headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'accessibleKnowledgeBase' in json_data['body']
        assert 'accessibleDocuments' in json_data['body']
        assert 'todayQuestions' in json_data['body']
    
    def test_get_list(self, client, db_session, auth_headers_user, knowledge_base):
        """测试获取知识库列表"""
        # Arrange
        data = {
            'page': 1,
            'pageSize': 20
        }
        
        # Act
        response = client.post('/api/knowledge-base/list', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'list' in json_data['body']
        assert 'total' in json_data['body']
        assert json_data['body']['total'] >= 1
    
    def test_get_list_with_keyword(self, client, db_session, auth_headers_user, knowledge_base):
        """测试关键词搜索知识库"""
        # Arrange
        data = {
            'keyword': '测试',
            'page': 1,
            'pageSize': 20
        }
        
        # Act
        response = client.post('/api/knowledge-base/list', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'list' in json_data['body']
    
    def test_get_detail(self, client, db_session, auth_headers_user, knowledge_base):
        """测试获取知识库详情"""
        # Arrange
        data = {
            'id': knowledge_base.id
        }
        
        # Act
        response = client.post('/api/knowledge-base/detail', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['id'] == knowledge_base.id
        assert json_data['body']['name'] == '测试知识库'
    
    def test_get_detail_not_found(self, client, db_session, auth_headers_user):
        """测试获取不存在的知识库"""
        # Arrange
        data = {
            'id': 'nonexistent_id'
        }
        
        # Act
        response = client.post('/api/knowledge-base/detail', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 2002
    
    def test_create_knowledge_base(self, client, db_session, auth_headers_admin):
        """测试创建知识库（管理员）"""
        # Arrange
        data = {
            'name': '新知识库',
            'code': 'new_kb',
            'description': '新建的知识库',
            'visible': 'all'
        }
        
        # Act
        response = client.post('/api/knowledge-base/create', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['name'] == '新知识库'
    
    def test_create_knowledge_base_duplicate_code(self, client, db_session, auth_headers_admin, knowledge_base):
        """测试创建重复编码的知识库"""
        # Arrange
        data = {
            'name': '重复知识库',
            'code': 'test_kb',  # 已存在的编码
            'description': '测试',
            'visible': 'all'
        }
        
        # Act
        response = client.post('/api/knowledge-base/create', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 2003
    
    def test_create_knowledge_base_missing_fields(self, client, db_session, auth_headers_admin):
        """测试缺少必填字段"""
        # Arrange
        data = {
            'name': '测试'
            # 缺少code
        }
        
        # Act
        response = client.post('/api/knowledge-base/create', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 2001
    
    def test_create_knowledge_base_non_admin(self, client, db_session, auth_headers_user):
        """测试非管理员创建知识库"""
        # Arrange
        data = {
            'name': '新知识库',
            'code': 'new_kb',
            'description': '测试'
        }
        
        # Act
        response = client.post('/api/knowledge-base/create', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 403
    
    def test_update_knowledge_base(self, client, db_session, auth_headers_admin, knowledge_base):
        """测试更新知识库"""
        # Arrange
        data = {
            'id': knowledge_base.id,
            'name': '更新的名称',
            'description': '更新的描述'
        }
        
        # Act
        response = client.post('/api/knowledge-base/update', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert json_data['body']['name'] == '更新的名称'
    
    def test_delete_knowledge_base(self, client, db_session, auth_headers_admin, knowledge_base):
        """测试删除知识库"""
        # Arrange
        data = {
            'id': knowledge_base.id
        }
        
        # Act
        response = client.post('/api/knowledge-base/delete', 
                              json=data, 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        
        # 验证已删除
        kb = KnowledgeBase.query.get(knowledge_base.id)
        assert kb is None
    
    def test_get_documents(self, client, db_session, auth_headers_user, knowledge_base):
        """测试获取文档列表"""
        # Arrange
        data = {
            'knowledgeBaseId': knowledge_base.id,
            'page': 1,
            'pageSize': 20
        }
        
        # Act
        response = client.post('/api/knowledge-base/documents', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'list' in json_data['body']
    
    def test_get_vector_models(self, client, db_session, auth_headers_admin, embedding_model):
        """测试获取向量模型列表"""
        # Act
        response = client.post('/api/knowledge-base/vector-models', 
                              headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert isinstance(json_data['body'], list)


