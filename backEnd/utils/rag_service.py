"""
RAG（Retrieval-Augmented Generation）服务
处理知识检索、向量化、LLM调用等核心功能
"""
import os
import time
import requests
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from chromadb.config import Settings
from flask import current_app


class RAGService:
    """RAG 服务类"""
    
    def __init__(self):
        """初始化 RAG 服务"""
        self.chroma_client = None
        self.ollama_base_url = None
        self.embedding_model = None
        self.default_llm_model = None
        
    def initialize(self, app=None):
        """
        初始化服务
        
        Args:
            app: Flask 应用实例
        """
        if app:
            self.ollama_base_url = app.config.get('OLLAMA_BASE_URL')
            self.embedding_model = app.config.get('EMBEDDING_MODEL_NAME')
            self.default_llm_model = app.config.get('LLM_DEFAULT_MODEL')
            
            # 初始化 ChromaDB 客户端
            persist_directory = app.config.get('CHROMA_PERSIST_DIRECTORY')
            self.chroma_client = chromadb.PersistentClient(
                path=persist_directory
            )
            
            app.logger.info(f'RAG 服务初始化完成: Ollama={self.ollama_base_url}, '
                          f'Embedding={self.embedding_model}, LLM={self.default_llm_model}')
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        获取文本的向量嵌入
        
        Args:
            texts: 文本列表
            
        Returns:
            向量列表
        """
        try:
            url = f"{self.ollama_base_url}/api/embeddings"
            
            embeddings = []
            for text in texts:
                response = requests.post(
                    url,
                    json={
                        "model": self.embedding_model,
                        "prompt": text
                    },
                    timeout=30
                )
                response.raise_for_status()
                result = response.json()
                embeddings.append(result.get('embedding', []))
            
            return embeddings
            
        except Exception as e:
            current_app.logger.error(f'获取嵌入向量失败: {str(e)}', exc_info=True)
            raise
    
    def get_or_create_collection(self, kb_id: str, kb_name: str = None):
        """
        获取或创建知识库的向量集合
        
        Args:
            kb_id: 知识库ID
            kb_name: 知识库名称（可选）
            
        Returns:
            ChromaDB 集合对象
        """
        try:
            collection_name = f"kb_{kb_id}"
            
            # 尝试获取现有集合
            try:
                collection = self.chroma_client.get_collection(name=collection_name)
                current_app.logger.info(f'使用现有向量集合: {collection_name}')
                return collection
            except:
                # 集合不存在，创建新集合
                collection = self.chroma_client.create_collection(
                    name=collection_name,
                    metadata={"kb_id": kb_id, "kb_name": kb_name or kb_id}
                )
                current_app.logger.info(f'创建新向量集合: {collection_name}')
                return collection
                
        except Exception as e:
            current_app.logger.error(f'获取或创建向量集合失败: {str(e)}', exc_info=True)
            raise
    
    def add_documents(self, kb_id: str, documents: List[Dict[str, Any]]):
        """
        向知识库添加文档
        
        Args:
            kb_id: 知识库ID
            documents: 文档列表，每个文档包含 id, content, metadata
        """
        try:
            collection = self.get_or_create_collection(kb_id)
            
            # 提取文档内容
            doc_ids = [doc['id'] for doc in documents]
            doc_contents = [doc['content'] for doc in documents]
            doc_metadatas = [doc.get('metadata', {}) for doc in documents]
            
            # 获取嵌入向量
            embeddings = self.get_embeddings(doc_contents)
            
            # 添加到向量库
            collection.add(
                ids=doc_ids,
                documents=doc_contents,
                embeddings=embeddings,
                metadatas=doc_metadatas
            )
            
            current_app.logger.info(f'向知识库 {kb_id} 添加了 {len(documents)} 个文档块')
            
        except Exception as e:
            current_app.logger.error(f'添加文档到向量库失败: {str(e)}', exc_info=True)
            raise
    
    def search_documents(
        self, 
        kb_id: str, 
        query: str, 
        top_k: int = 5,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        在知识库中检索相关文档
        
        Args:
            kb_id: 知识库ID
            query: 查询文本
            top_k: 返回最相关的前N个结果
            similarity_threshold: 相似度阈值（0-1之间）
            
        Returns:
            检索结果列表
        """
        try:
            collection = self.get_or_create_collection(kb_id)
            
            # 获取查询向量
            query_embedding = self.get_embeddings([query])[0]
            
            # 检索相关文档
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=['documents', 'metadatas', 'distances']
            )
            
            # 处理结果
            documents = []
            if results and results['ids']:
                for i, doc_id in enumerate(results['ids'][0]):
                    # 计算相似度 (ChromaDB 返回的是距离，需要转换为相似度)
                    distance = results['distances'][0][i]
                    similarity = 1 / (1 + distance)  # 简单的距离转相似度公式
                    
                    # 过滤低于阈值的结果
                    if similarity >= similarity_threshold:
                        documents.append({
                            'id': doc_id,
                            'content': results['documents'][0][i],
                            'metadata': results['metadatas'][0][i],
                            'similarity': round(similarity, 4)
                        })
            
            current_app.logger.info(f'在知识库 {kb_id} 中检索到 {len(documents)} 个相关文档')
            return documents
            
        except Exception as e:
            current_app.logger.error(f'检索文档失败: {str(e)}', exc_info=True)
            return []
    
    def generate_answer(
        self,
        question: str,
        context_documents: List[Dict[str, Any]],
        model_name: str = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        使用 LLM 生成答案
        
        Args:
            question: 用户问题
            context_documents: 检索到的上下文文档
            model_name: 使用的模型名称（如不指定则使用默认模型）
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            (答案文本, 引用列表)
        """
        try:
            # 使用默认值
            if not model_name:
                model_name = self.default_llm_model
            if temperature is None:
                temperature = current_app.config.get('LLM_TEMPERATURE', 0.7)
            if max_tokens is None:
                max_tokens = current_app.config.get('LLM_MAX_TOKENS', 2048)
            
            # 构建上下文
            context = self._build_context(context_documents)
            
            # 构建提示词
            prompt = self._build_prompt(question, context)
            
            # 调用 Ollama API（兼容 OpenAI 格式）
            url = f"{self.ollama_base_url}/v1/chat/completions"
            
            response = requests.post(
                url,
                json={
                    "model": model_name,
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一个专业的知识库助手，能够根据提供的上下文信息准确回答用户的问题。"
                                     "如果上下文中没有相关信息，请如实告知用户。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                },
                timeout=current_app.config.get('LLM_TIMEOUT', 120)
            )
            response.raise_for_status()
            
            result = response.json()
            answer = result['choices'][0]['message']['content']
            
            # 构建引用列表
            references = self._build_references(context_documents)
            
            current_app.logger.info(f'使用模型 {model_name} 生成了答案')
            return answer, references
            
        except Exception as e:
            current_app.logger.error(f'生成答案失败: {str(e)}', exc_info=True)
            raise
    
    def _build_context(self, documents: List[Dict[str, Any]]) -> str:
        """
        构建上下文文本
        
        Args:
            documents: 文档列表
            
        Returns:
            上下文文本
        """
        if not documents:
            return "没有找到相关的上下文信息。"
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            
            # 添加来源信息（如果有）
            source = metadata.get('source', f'文档{i}')
            context_parts.append(f"[来源: {source}]\n{content}")
        
        return "\n\n---\n\n".join(context_parts)
    
    def _build_prompt(self, question: str, context: str) -> str:
        """
        构建完整的提示词
        
        Args:
            question: 用户问题
            context: 上下文信息
            
        Returns:
            完整的提示词
        """
        prompt = f"""请基于以下上下文信息回答用户的问题。

【上下文信息】
{context}

【用户问题】
{question}

【回答要求】
1. 仅基于上述上下文信息进行回答
2. 如果上下文中没有相关信息，请明确告知用户
3. 回答要准确、简洁、有条理
4. 可以引用具体的来源信息

请回答："""
        
        return prompt
    
    def _build_references(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        构建引用列表
        
        Args:
            documents: 文档列表
            
        Returns:
            引用列表
        """
        references = []
        for doc in documents:
            metadata = doc.get('metadata', {})
            references.append({
                'documentId': metadata.get('document_id', ''),
                'documentName': metadata.get('document_name', '未知文档'),
                'chunkId': doc.get('id', ''),
                'similarity': doc.get('similarity', 0),
                'content': doc.get('content', '')[:200] + '...'  # 摘录前200字符
            })
        
        return references
    
    def chat(
        self,
        question: str,
        kb_id: str = None,
        model_name: str = None,
        top_k: int = 5,
        similarity_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        完整的 RAG 问答流程
        
        Args:
            question: 用户问题
            kb_id: 知识库ID（可选，如果不指定则不使用知识库）
            model_name: 使用的模型名称
            top_k: 检索文档数量
            similarity_threshold: 相似度阈值
            
        Returns:
            包含答案和引用的字典
        """
        try:
            context_documents = []
            
            # 如果指定了知识库，则检索相关文档
            if kb_id:
                context_documents = self.search_documents(
                    kb_id=kb_id,
                    query=question,
                    top_k=top_k,
                    similarity_threshold=similarity_threshold
                )
            
            # 生成答案
            answer, references = self.generate_answer(
                question=question,
                context_documents=context_documents,
                model_name=model_name
            )
            
            return {
                'answer': answer,
                'references': references,
                'context_count': len(context_documents)
            }
            
        except Exception as e:
            current_app.logger.error(f'RAG 问答失败: {str(e)}', exc_info=True)
            raise
    
    def check_ollama_health(self) -> Dict[str, Any]:
        """
        检查 Ollama 服务健康状态
        
        Returns:
            健康状态信息
        """
        try:
            url = f"{self.ollama_base_url}/api/tags"
            start_time = time.time()
            
            response = requests.get(url, timeout=5)
            response_time = int((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                return {
                    'status': 'online',
                    'response_time': response_time,
                    'available_models': [m['name'] for m in models],
                    'message': f'Ollama 服务正常，可用模型: {len(models)} 个'
                }
            else:
                return {
                    'status': 'error',
                    'response_time': response_time,
                    'message': f'Ollama 服务响应异常: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'status': 'offline',
                'response_time': None,
                'message': f'无法连接到 Ollama 服务: {str(e)}'
            }
    
    def delete_collection(self, kb_id: str):
        """
        删除知识库的向量集合
        
        Args:
            kb_id: 知识库ID
        """
        try:
            collection_name = f"kb_{kb_id}"
            self.chroma_client.delete_collection(name=collection_name)
            current_app.logger.info(f'删除向量集合: {collection_name}')
        except Exception as e:
            current_app.logger.error(f'删除向量集合失败: {str(e)}', exc_info=True)
            raise


# 全局 RAG 服务实例
rag_service = RAGService()

