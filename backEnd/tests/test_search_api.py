"""
搜索API测试
测试文档搜索、热门关键词等功能
"""
import pytest


@pytest.mark.api
class TestSearchAPI:
    """搜索API测试类"""
    
    def test_search_documents(self, client, db_session, auth_headers_user):
        """测试搜索文档"""
        # Arrange
        data = {
            'keyword': '测试关键词',
            'knowledgeBaseId': 'all',
            'docType': 'all',
            'sortBy': 'relevance',
            'page': 1,
            'pageSize': 10
        }
        
        # Act
        response = client.post('/api/search/documents', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'list' in json_data['body']
        assert 'total' in json_data['body']
    
    def test_search_documents_no_keyword(self, client, db_session, auth_headers_user):
        """测试空关键词搜索"""
        # Arrange
        data = {
            'keyword': ''
        }
        
        # Act
        response = client.post('/api/search/documents', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 4001
    
    def test_get_hot_keywords(self, client, db_session, auth_headers_user):
        """测试获取热门关键词"""
        # Arrange
        data = {
            'limit': 10
        }
        
        # Act
        response = client.post('/api/search/hot-keywords', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert isinstance(json_data['body'], list)
    
    def test_get_doc_types(self, client, db_session, auth_headers_user):
        """测试获取文档类型列表"""
        # Act
        response = client.post('/api/search/doc-types', headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert isinstance(json_data['body'], list)
        assert len(json_data['body']) > 0
    
    def test_export_search_not_implemented(self, client, db_session, auth_headers_user):
        """测试导出搜索结果（未实现）"""
        # Act
        response = client.post('/api/search/export', headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 4002


