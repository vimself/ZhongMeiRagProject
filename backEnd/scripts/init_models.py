"""
初始化模型数据脚本
在数据库中添加 Ollama 模型记录
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models.model import Model
from utils.helpers import generate_id
from datetime import datetime


def init_ollama_models():
    """初始化 Ollama 模型"""
    app = create_app()
    
    with app.app_context():
        print('=' * 60)
        print('开始初始化 Ollama 模型')
        print('=' * 60)
        
        # 获取配置
        ollama_base_url = app.config.get('OLLAMA_BASE_URL')
        
        # 定义模型配置
        models_to_add = [
            {
                'name': 'qwen3:4b',
                'type': 'llm',
                'description': 'Qwen3 4B 模型 - 通义千问3代4B参数版本，平衡性能与速度',
                'provider': 'ollama',
                'endpoint': ollama_base_url,
                'status': 'online',
                'is_default': True,  # 设为默认模型
                'model_size': '2.5 GB',
                'context_length': 32768,
                'config': {
                    'temperature': 0.7,
                    'max_tokens': 2048,
                    'top_p': 0.9,
                    'top_k': 40
                }
            },
            {
                'name': 'llama3.2:3b',
                'type': 'llm',
                'description': 'Llama 3.2 3B 模型 - Meta开源的轻量级语言模型',
                'provider': 'ollama',
                'endpoint': ollama_base_url,
                'status': 'online',
                'is_default': False,
                'model_size': '2.0 GB',
                'context_length': 8192,
                'config': {
                    'temperature': 0.7,
                    'max_tokens': 2048,
                    'top_p': 0.9,
                    'top_k': 40
                }
            },
            {
                'name': 'dengcao/Qwen3-Embedding-4B:Q5_K_M',
                'type': 'embedding',
                'description': 'Qwen3 嵌入模型 - 用于文本向量化和语义检索',
                'provider': 'ollama',
                'endpoint': ollama_base_url,
                'status': 'online',
                'is_default': True,  # 设为默认嵌入模型
                'model_size': '2.9 GB',
                'context_length': 8192,
                'config': {
                    'dimension': 768,
                    'normalize': True
                }
            }
        ]
        
        # 添加或更新模型
        for model_config in models_to_add:
            model_name = model_config['name']
            
            # 检查模型是否已存在
            existing_model = Model.query.filter_by(name=model_name).first()
            
            if existing_model:
                print(f'\n更新现有模型: {model_name}')
                # 更新模型信息
                for key, value in model_config.items():
                    if key != 'name':
                        setattr(existing_model, key, value)
                existing_model.updated_at = datetime.utcnow()
                model = existing_model
            else:
                print(f'\n添加新模型: {model_name}')
                # 创建新模型
                model = Model(
                    id=generate_id('model'),
                    **model_config,
                    created_at=datetime.utcnow()
                )
                db.session.add(model)
            
            # 打印模型信息
            print(f'  类型: {model_config["type"]}')
            print(f'  描述: {model_config["description"]}')
            print(f'  大小: {model_config["model_size"]}')
            print(f'  状态: {model_config["status"]}')
            print(f'  默认: {"是" if model_config["is_default"] else "否"}')
        
        # 提交更改
        try:
            db.session.commit()
            print('\n' + '=' * 60)
            print('✓ 模型初始化成功！')
            print('=' * 60)
            
            # 显示所有模型
            print('\n当前系统中的所有模型:')
            all_models = Model.query.all()
            
            print('\nLLM 模型:')
            for m in filter(lambda x: x.type == 'llm', all_models):
                default_tag = ' [默认]' if m.is_default else ''
                print(f'  - {m.name}{default_tag} ({m.status})')
            
            print('\n嵌入模型:')
            for m in filter(lambda x: x.type == 'embedding', all_models):
                default_tag = ' [默认]' if m.is_default else ''
                print(f'  - {m.name}{default_tag} ({m.status})')
            
            print('\n提示: 你可以在前端界面中切换使用不同的模型')
            
        except Exception as e:
            db.session.rollback()
            print(f'\n✗ 错误: 模型初始化失败 - {str(e)}')
            import traceback
            traceback.print_exc()
            return False
        
        return True


def check_ollama_service():
    """检查 Ollama 服务状态"""
    app = create_app()
    
    with app.app_context():
        from utils.rag_service import rag_service
        
        print('\n检查 Ollama 服务状态...')
        
        try:
            # 初始化 RAG 服务
            rag_service.initialize(app)
            
            # 检查服务健康状态
            health = rag_service.check_ollama_health()
            
            print(f'\n服务状态: {health["status"]}')
            print(f'消息: {health["message"]}')
            
            if health['status'] == 'online':
                print('\n可用模型:')
                for model_name in health.get('available_models', []):
                    print(f'  - {model_name}')
                return True
            else:
                print('\n⚠ 警告: Ollama 服务未运行或无法访问')
                print('请确保:')
                print('1. Ollama 已安装: https://ollama.ai')
                print('2. Ollama 服务正在运行')
                print('3. 已拉取所需的模型')
                return False
                
        except Exception as e:
            print(f'\n✗ 检查失败: {str(e)}')
            return False


def main():
    """主函数"""
    print('Ollama 模型初始化工具')
    print('=' * 60)
    
    # 先检查 Ollama 服务
    service_ok = check_ollama_service()
    
    # 无论服务是否可用，都继续初始化模型记录
    print('\n' + '=' * 60)
    success = init_ollama_models()
    
    if success:
        if not service_ok:
            print('\n⚠ 注意: 模型记录已创建，但 Ollama 服务不可用')
            print('请启动 Ollama 服务后再使用系统')
        print('\n完成！')
        return 0
    else:
        print('\n初始化失败')
        return 1


if __name__ == '__main__':
    sys.exit(main())

