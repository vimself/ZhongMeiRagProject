"""
管理员仪表板API测试
测试统计数据、系统状态等功能
"""
import pytest


@pytest.mark.api
@pytest.mark.admin
class TestDashboardAPI:
    """仪表板API测试类"""
    
    def test_get_stats(self, client, db_session, auth_headers_admin):
        """测试获取统计数据"""
        # Act
        response = client.post('/api/dashboard/stats', headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'todayQuestions' in json_data['body']
        assert 'searchCount' in json_data['body']
        assert 'knowledgeBaseCount' in json_data['body']
        assert 'documentCount' in json_data['body']
    
    def test_get_stats_non_admin(self, client, db_session, auth_headers_user):
        """测试非管理员访问统计数据"""
        # Act
        response = client.post('/api/dashboard/stats', headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 403
    
    def test_get_system_status(self, client, db_session, auth_headers_admin, llm_model, embedding_model):
        """测试获取系统状态"""
        # Act
        response = client.post('/api/dashboard/system-status', headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'llmModel' in json_data['body']
        assert 'vectorModel' in json_data['body']
        assert 'vectorDb' in json_data['body']
        assert 'relationalDb' in json_data['body']
        assert 'systemStatus' in json_data['body']
    
    def test_refresh_status(self, client, db_session, auth_headers_admin):
        """测试刷新系统状态"""
        # Act
        response = client.post('/api/dashboard/refresh-status', headers=auth_headers_admin)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0

