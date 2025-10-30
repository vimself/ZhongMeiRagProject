"""
聊天对话API测试
测试会话管理、消息发送等功能
"""
import pytest


@pytest.mark.api
class TestChatAPI:
    """聊天API测试类"""
    
    def test_get_knowledge_bases(self, client, db_session, auth_headers_user, knowledge_base):
        """测试获取知识库列表"""
        # Act
        response = client.post('/api/chat/knowledge-bases', headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert isinstance(json_data['body'], list)
        assert len(json_data['body']) >= 1
    
    def test_get_models(self, client, db_session, auth_headers_user, llm_model):
        """测试获取模型列表"""
        # Act
        response = client.post('/api/chat/models', headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert isinstance(json_data['body'], list)
        assert len(json_data['body']) >= 1
    
    def test_get_sessions(self, client, db_session, auth_headers_user, chat_session):
        """测试获取会话历史"""
        # Arrange
        data = {
            'limit': 20
        }
        
        # Act
        response = client.post('/api/chat/sessions', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert isinstance(json_data['body'], list)
    
    def test_create_session(self, client, db_session, auth_headers_user, knowledge_base, llm_model):
        """测试创建会话"""
        # Arrange
        data = {
            'knowledgeBaseId': knowledge_base.id,
            'modelId': llm_model.id
        }
        
        # Act
        response = client.post('/api/chat/session/create', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'id' in json_data['body']
        assert json_data['body']['title'] == '新对话'
    
    def test_create_session_missing_params(self, client, db_session, auth_headers_user):
        """测试缺少参数"""
        # Arrange
        data = {
            # 缺少必需参数
        }
        
        # Act
        response = client.post('/api/chat/session/create', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 3001
    
    def test_send_message(self, client, db_session, auth_headers_user, chat_session):
        """测试发送消息"""
        # Arrange
        data = {
            'sessionId': chat_session.id,
            'question': '这是一个测试问题'
        }
        
        # Act
        response = client.post('/api/chat/message/send', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert 'answer' in json_data['body']
        assert 'references' in json_data['body']
    
    def test_send_message_too_long(self, client, db_session, auth_headers_user, chat_session):
        """测试问题过长"""
        # Arrange
        data = {
            'sessionId': chat_session.id,
            'question': 'a' * 1001  # 超过1000字符
        }
        
        # Act
        response = client.post('/api/chat/message/send', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 3002
    
    def test_send_message_session_not_found(self, client, db_session, auth_headers_user):
        """测试会话不存在"""
        # Arrange
        data = {
            'sessionId': 'nonexistent',
            'question': '测试问题'
        }
        
        # Act
        response = client.post('/api/chat/message/send', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 3003
    
    def test_get_session_messages(self, client, db_session, auth_headers_user, chat_session):
        """测试获取会话消息"""
        # Arrange
        data = {
            'sessionId': chat_session.id
        }
        
        # Act
        response = client.post('/api/chat/session/messages', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
        assert isinstance(json_data['body'], list)
    
    def test_delete_session(self, client, db_session, auth_headers_user, chat_session):
        """测试删除会话"""
        # Arrange
        data = {
            'sessionId': chat_session.id
        }
        
        # Act
        response = client.post('/api/chat/session/delete', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0
    
    def test_rename_session(self, client, db_session, auth_headers_user, chat_session):
        """测试重命名会话"""
        # Arrange
        data = {
            'sessionId': chat_session.id,
            'title': '新标题'
        }
        
        # Act
        response = client.post('/api/chat/session/rename', 
                              json=data, 
                              headers=auth_headers_user)
        
        # Assert
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['error'] == 0

