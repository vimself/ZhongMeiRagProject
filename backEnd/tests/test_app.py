"""
应用基础测试
测试健康检查、错误处理等基础功能
"""
import pytest


@pytest.mark.api
class TestApp:
    """应用基础测试类"""
    
    def test_health_check(self, client):
        """测试健康检查接口"""
        # Act
        response = client.get('/health')
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['status'] == 'healthy'
        assert json_data['service'] == 'RAG Knowledge Base API'
    
    def test_404_not_found(self, client):
        """测试404错误"""
        # Act
        response = client.get('/api/nonexistent')
        
        # Assert
        assert response.status_code == 404
    
    def test_app_config(self, app):
        """测试应用配置"""
        # Assert
        assert app.config['TESTING'] is True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'

