# Chroma向量数据库使用说明

> **文档版本**: v1.0  
> **更新日期**: 2025-10-17  
> **适用项目**: RAG知识问答系统

---

## 目录

1. [Chroma简介](#1-chroma简介)
2. [安装与配置](#2-安装与配置)
3. [基本使用](#3-基本使用)
4. [RAG项目集成](#4-rag项目集成)
5. [常见问题](#5-常见问题)
6. [性能优化](#6-性能优化)

---

## 1. Chroma简介

### 什么是Chroma？

Chroma是一个开源的向量数据库，专为AI应用设计。它的主要特点：

- **轻量级**: 易于安装和部署，支持本地运行
- **易用性**: Python API简洁直观
- **高性能**: 基于SQLite和DuckDB，查询速度快
- **灵活性**: 支持多种向量化模型和距离算法

### 为什么选择Chroma？

在RAG（Retrieval-Augmented Generation）系统中，Chroma用于：

1. **存储文档向量**: 将文档切片转换为向量后存储
2. **语义检索**: 根据问题向量检索最相关的文档片段
3. **快速查询**: 毫秒级响应，支持TopK检索

---

## 2. 安装与配置

### 2.1 安装Chroma

Chroma已包含在项目依赖中，运行以下命令安装：

```bash
cd backEnd
pip install -r requirements.txt
```

或单独安装：

```bash
pip install chromadb==0.4.15
```

### 2.2 配置路径

在 `.env` 文件中配置Chroma数据存储路径：

```ini
# 向量数据库配置
CHROMA_PERSIST_DIRECTORY=./chroma_db
EMBEDDING_MODEL_NAME=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### 2.3 初始化Chroma客户端

在项目中创建Chroma客户端：

```python
import chromadb
from chromadb.config import Settings

# 创建持久化客户端
client = chromadb.Client(Settings(
    persist_directory="./chroma_db",
    anonymized_telemetry=False
))
```

---

## 3. 基本使用

### 3.1 创建Collection

Collection是Chroma中的数据集合，类似于关系数据库中的表。

```python
# 创建或获取collection
collection = client.get_or_create_collection(
    name="knowledge_base_001",
    metadata={"description": "技术规范知识库"}
)
```

### 3.2 添加文档

将文档切片添加到collection：

```python
# 添加文档向量
collection.add(
    documents=["这是第一段文档内容", "这是第二段文档内容"],
    metadatas=[
        {"source": "doc_001", "page": 1},
        {"source": "doc_001", "page": 2}
    ],
    ids=["chunk_001", "chunk_002"]
)
```

**参数说明**：
- `documents`: 文档文本列表（Chroma会自动向量化）
- `metadatas`: 元数据列表，用于存储额外信息
- `ids`: 唯一标识符列表

### 3.3 查询文档

根据查询文本检索相关文档：

```python
# 语义检索
results = collection.query(
    query_texts=["如何实现用户认证？"],
    n_results=5  # TopK
)

# 解析结果
for i, doc in enumerate(results['documents'][0]):
    print(f"相关度排名 {i+1}:")
    print(f"内容: {doc}")
    print(f"相似度: {results['distances'][0][i]}")
    print(f"元数据: {results['metadatas'][0][i]}")
    print()
```

### 3.4 更新和删除

```python
# 更新文档
collection.update(
    ids=["chunk_001"],
    documents=["更新后的文档内容"],
    metadatas=[{"source": "doc_001", "page": 1, "updated": True}]
)

# 删除文档
collection.delete(ids=["chunk_001"])

# 删除整个collection
client.delete_collection(name="knowledge_base_001")
```

---

## 4. RAG项目集成

### 4.1 项目结构

在项目中创建向量数据库服务模块：

```
backEnd/
├── services/
│   ├── __init__.py
│   ├── chroma_service.py      # Chroma服务
│   ├── embedding_service.py   # 向量化服务
│   └── rag_service.py          # RAG服务
```

### 4.2 Chroma服务实现

创建 `services/chroma_service.py`：

```python
"""
Chroma向量数据库服务
"""
import chromadb
from chromadb.config import Settings
from flask import current_app


class ChromaService:
    """Chroma服务类"""
    
    def __init__(self):
        self.client = None
    
    def init_client(self):
        """初始化Chroma客户端"""
        persist_dir = current_app.config['CHROMA_PERSIST_DIRECTORY']
        
        self.client = chromadb.Client(Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False
        ))
    
    def get_collection(self, kb_id):
        """获取或创建知识库collection"""
        if not self.client:
            self.init_client()
        
        return self.client.get_or_create_collection(
            name=f"kb_{kb_id}",
            metadata={"kb_id": kb_id}
        )
    
    def add_documents(self, kb_id, chunks):
        """
        添加文档切片
        
        Args:
            kb_id: 知识库ID
            chunks: 切片列表，每个切片包含 {id, text, metadata}
        """
        collection = self.get_collection(kb_id)
        
        documents = [chunk['text'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]
        ids = [chunk['id'] for chunk in chunks]
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, kb_id, query, top_k=5):
        """
        检索相关文档
        
        Args:
            kb_id: 知识库ID
            query: 查询文本
            top_k: 返回结果数量
        
        Returns:
            检索结果列表
        """
        collection = self.get_collection(kb_id)
        
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # 格式化结果
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'score': 1 - results['distances'][0][i]  # 转换为相似度
            })
        
        return formatted_results
    
    def delete_collection(self, kb_id):
        """删除知识库collection"""
        if not self.client:
            self.init_client()
        
        try:
            self.client.delete_collection(name=f"kb_{kb_id}")
        except Exception as e:
            current_app.logger.error(f'删除collection失败: {str(e)}')


# 创建全局实例
chroma_service = ChromaService()
```

### 4.3 使用示例

在API接口中使用Chroma服务：

```python
from services.chroma_service import chroma_service

# 添加文档
def add_document_to_kb(kb_id, document_id, chunks):
    """将文档添加到知识库"""
    chunk_data = []
    for i, chunk_text in enumerate(chunks):
        chunk_data.append({
            'id': f'{document_id}_chunk_{i}',
            'text': chunk_text,
            'metadata': {
                'document_id': document_id,
                'kb_id': kb_id,
                'chunk_index': i
            }
        })
    
    chroma_service.add_documents(kb_id, chunk_data)

# 检索文档
def search_knowledge(kb_id, question, top_k=5):
    """从知识库检索"""
    results = chroma_service.search(kb_id, question, top_k)
    return results
```

### 4.4 文档处理流程

```python
def process_document(kb_id, file_path):
    """
    处理文档流程
    1. 解析PDF
    2. 文本切片
    3. 向量化并存储
    """
    # 1. 解析PDF
    text = extract_text_from_pdf(file_path)
    
    # 2. 文本切片
    chunks = split_text(text, chunk_size=500, overlap=50)
    
    # 3. 存储到Chroma
    document_id = generate_id('doc')
    add_document_to_kb(kb_id, document_id, chunks)
    
    return document_id
```

---

## 5. 常见问题

### Q1: Chroma数据存储在哪里？

**答**: Chroma数据存储在配置的 `CHROMA_PERSIST_DIRECTORY` 目录中（默认 `./chroma_db`）。该目录包含SQLite数据库文件和向量索引。

### Q2: 如何备份Chroma数据？

**答**: 直接备份整个 `chroma_db` 目录即可：

```bash
# 备份
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz chroma_db/

# 恢复
tar -xzf chroma_backup_20251017.tar.gz
```

### Q3: 支持哪些向量化模型？

**答**: Chroma支持任何生成向量的模型，推荐中文模型：

- **BGE-M3**: 通用中文向量模型（推荐）
- **M3E**: 多语言模型
- **text-embedding-ada-002**: OpenAI模型（需要API Key）

### Q4: 如何切换向量化模型？

**答**: Chroma默认使用内置的sentence-transformers模型。如需使用自定义模型：

```python
from chromadb.utils import embedding_functions

# 使用OpenAI模型
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="your-api-key",
    model_name="text-embedding-ada-002"
)

collection = client.create_collection(
    name="my_collection",
    embedding_function=openai_ef
)
```

### Q5: Chroma的查询性能如何？

**答**: 
- 小规模（< 10万条）：< 100ms
- 中规模（10万-100万条）：< 500ms
- 大规模（> 100万条）：考虑使用Milvus或Qdrant

### Q6: 如何清空所有数据？

**答**: 

```bash
# 删除整个目录
rm -rf chroma_db/

# 或在Python中
client.reset()  # 清空所有collection
```

---

## 6. 性能优化

### 6.1 批量操作

使用批量添加提升性能：

```python
# ❌ 低效：逐条添加
for chunk in chunks:
    collection.add(documents=[chunk['text']], ids=[chunk['id']])

# ✅ 高效：批量添加
collection.add(
    documents=[c['text'] for c in chunks],
    ids=[c['id'] for c in chunks]
)
```

### 6.2 合理设置TopK

TopK越大，查询越慢：

```python
# 根据场景选择合适的TopK
collection.query(query_texts=[query], n_results=5)  # 推荐5-10
```

### 6.3 使用过滤条件

利用metadata过滤减少搜索范围：

```python
results = collection.query(
    query_texts=[query],
    n_results=5,
    where={"source": "doc_001"}  # 只在特定文档中搜索
)
```

### 6.4 定期优化

定期重建索引以保持性能：

```python
# 删除并重建collection
client.delete_collection(name="my_collection")
collection = client.create_collection(name="my_collection")
# 重新添加数据
```

---

## 7. 进阶话题

### 7.1 自定义距离算法

Chroma支持多种距离算法：

```python
collection = client.create_collection(
    name="my_collection",
    metadata={"hnsw:space": "cosine"}  # cosine, l2, ip
)
```

### 7.2 多知识库管理

为每个知识库创建独立的collection：

```python
# 知识库1
kb1_collection = client.get_or_create_collection(name="kb_001")

# 知识库2
kb2_collection = client.get_or_create_collection(name="kb_002")
```

### 7.3 监控和日志

记录查询性能：

```python
import time

start = time.time()
results = collection.query(query_texts=[query], n_results=5)
duration = time.time() - start

logger.info(f"Chroma查询耗时: {duration:.3f}秒")
```

---

## 8. 参考资料

- **Chroma官方文档**: https://docs.trychroma.com/
- **GitHub仓库**: https://github.com/chroma-core/chroma
- **RAG最佳实践**: https://www.pinecone.io/learn/retrieval-augmented-generation/

---

**注意事项**:
1. Chroma适合中小规模应用，大规模请考虑Milvus或Qdrant
2. 定期备份 `chroma_db` 目录
3. 生产环境建议使用SSD存储以提升性能

