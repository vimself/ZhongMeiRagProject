# ChromaDB 向量数据库集成说明

> **文档版本**: v2.0  
> **更新日期**: 2025-10-31  
> **适用项目**: RAG 知识问答系统

---

## 概述

本系统使用 ChromaDB 作为向量数据库，配合 Ollama 嵌入模型实现文档的语义检索功能。

### 技术架构

```
文档上传
   ↓
解析文档（PDF/Word/TXT）
   ↓
智能分块（500字/块，50字重叠）
   ↓
Ollama 向量化（Qwen3-Embedding-4B）
   ↓
存储到 ChromaDB
   ↓
支持语义检索
```

---

## 核心功能

### 1. 文档处理流程

#### 1.1 文档上传

```python
POST /api/knowledge-base/upload-document
Content-Type: multipart/form-data

参数:
- file: 文档文件（PDF/Word/TXT）
- knowledgeBaseId: 知识库ID
```

**处理流程**:
1. 验证文件类型和权限
2. 保存文件到 `uploads/` 目录
3. 解析文档提取文本
4. 智能分块（默认 500 字/块，50 字重叠）
5. 调用 Ollama 嵌入模型向量化
6. 存储到 ChromaDB
7. 保存文档元数据到数据库

#### 1.2 文档删除

```python
POST /api/knowledge-base/delete-document
Content-Type: application/json

{
  "documentId": "doc_xxx"
}
```

**处理流程**:
1. 从 ChromaDB 删除文档的所有向量块
2. 删除物理文件
3. 删除数据库记录

### 2. 语义检索流程

```python
# 用户提问
question = "如何实现用户认证？"

# 1. 问题向量化
query_embedding = ollama.embed(question)

# 2. ChromaDB 检索
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5  # TOP_K
)

# 3. 获取相关文档片段
# 4. 组装提示词发送给 LLM
# 5. 生成答案并返回引用
```

---

## 配置说明

### 环境变量

```bash
# ChromaDB 存储目录
CHROMA_PERSIST_DIRECTORY=chroma_db

# 嵌入模型（Ollama）
EMBEDDING_MODEL_NAME=dengcao/Qwen3-Embedding-4B:Q5_K_M
EMBEDDING_DIMENSION=768

# 分块参数
CHUNK_SIZE=500          # 每块字符数
CHUNK_OVERLAP=50        # 重叠字符数

# 检索参数
TOP_K=5                 # 检索返回数量
SIMILARITY_THRESHOLD=0.7 # 相似度阈值
```

### 目录结构

```
backEnd/
├── chroma_db/              # ChromaDB 数据目录
│   ├── chroma.sqlite3     # 元数据数据库
│   └── ...                # 向量索引文件
├── uploads/               # 上传文档目录
├── utils/
│   ├── rag_service.py     # RAG 服务（包含 ChromaDB 操作）
│   └── document_processor.py  # 文档处理服务
└── api/
    └── knowledge_base.py  # 知识库 API
```

---

## 核心代码

### 文档处理器

```python
# utils/document_processor.py

class DocumentProcessor:
    """文档处理器"""
    
    @staticmethod
    def extract_text(file_path, file_type):
        """提取文档文本"""
        if file_type == 'pdf':
            return extract_text_from_pdf(file_path)
        elif file_type in ['doc', 'docx']:
            return extract_text_from_word(file_path)
        elif file_type == 'txt':
            return extract_text_from_txt(file_path)
    
    @staticmethod
    def split_text(text, chunk_size=500, chunk_overlap=50):
        """智能分块"""
        # 按段落、句子等自然分隔符分块
        # 保持语义完整性
        return chunks
```

### RAG 服务

```python
# utils/rag_service.py

class RAGService:
    """RAG 服务"""
    
    def add_documents(self, kb_id, chunks):
        """添加文档到向量库"""
        collection = self.get_or_create_collection(kb_id)
        
        # 获取嵌入向量
        embeddings = self.get_embeddings([c['content'] for c in chunks])
        
        # 存储到 ChromaDB
        collection.add(
            ids=[c['id'] for c in chunks],
            documents=[c['content'] for c in chunks],
            embeddings=embeddings,
            metadatas=[c['metadata'] for c in chunks]
        )
    
    def search_documents(self, kb_id, query, top_k=5):
        """检索相关文档"""
        collection = self.get_or_create_collection(kb_id)
        
        # 问题向量化
        query_embedding = self.get_embeddings([query])[0]
        
        # 检索
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return results
```

---

## 使用示例

### 1. 上传文档

```bash
curl -X POST http://localhost:8000/api/knowledge-base/upload-document \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf" \
  -F "knowledgeBaseId=kb_xxx"
```

**响应**:
```json
{
  "error": 0,
  "message": "文档上传成功",
  "body": {
    "documentId": "doc_xxx",
    "documentName": "document.pdf",
    "chunkCount": 25,
    "fileSize": 1024000
  }
}
```

### 2. 智能问答

```bash
curl -X POST http://localhost:8000/api/chat/message/send \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "session_xxx",
    "question": "如何实现用户认证？"
  }'
```

**系统处理**:
1. 问题向量化（Ollama Embedding）
2. ChromaDB 检索相关文档片段
3. 组装提示词（问题 + 上下文）
4. LLM 生成回答（qwen3:4b）
5. 返回答案和引用来源

**响应**:
```json
{
  "error": 0,
  "message": "success",
  "body": {
    "answer": "用户认证可以通过以下方式实现...",
    "references": [
      {
        "documentId": "doc_xxx",
        "documentName": "开发文档.pdf",
        "similarity": 0.92,
        "content": "用户认证模块使用 JWT 令牌..."
      }
    ]
  }
}
```

---

## 性能优化

### 1. 分块策略

```python
# 推荐配置
CHUNK_SIZE=500      # 较小的块提高检索精度
CHUNK_OVERLAP=50    # 重叠保证语义连续性

# 大文档优化
CHUNK_SIZE=800      # 增大块大小
CHUNK_OVERLAP=100   # 增大重叠
```

### 2. 检索优化

```python
# 根据场景调整 TOP_K
TOP_K=3             # 快速响应
TOP_K=5             # 平衡质量（推荐）
TOP_K=10            # 高质量回答
```

### 3. 相似度阈值

```python
SIMILARITY_THRESHOLD=0.7   # 标准阈值
SIMILARITY_THRESHOLD=0.8   # 严格模式（更精确）
SIMILARITY_THRESHOLD=0.6   # 宽松模式（召回率高）
```

---

## 数据管理

### 备份 ChromaDB

```bash
# 备份整个 chroma_db 目录
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz chroma_db/

# 恢复
tar -xzf chroma_backup_20251031.tar.gz
```

### 清空数据

```bash
# 删除所有向量数据
rm -rf chroma_db/

# 系统会自动重建目录结构
```

### 查看存储

```bash
# 查看 ChromaDB 存储大小
du -sh chroma_db/

# 查看上传文件大小
du -sh uploads/
```

---

## 故障排查

### 问题 1: 文档上传失败

**症状**: 提示 "文档内容为空或无法解析"

**解决**:
1. 确认文件格式正确（PDF/Word/TXT）
2. 检查文件内容不为空
3. PDF 文件确保可以复制文本（非扫描版）

### 问题 2: 检索结果不相关

**症状**: 返回的文档片段与问题无关

**解决**:
1. 提高相似度阈值 `SIMILARITY_THRESHOLD`
2. 减少 `TOP_K` 值
3. 优化文档内容质量
4. 检查嵌入模型是否正常

### 问题 3: 向量化速度慢

**症状**: 文档上传耗时过长

**解决**:
1. 确认 Ollama 服务运行正常
2. 检查是否有 GPU 加速
3. 考虑使用批量处理
4. 减小文档大小或分批上传

---

## 监控和日志

### 查看日志

```bash
# 实时查看日志
tail -f backEnd/logs/app.log | grep -E 'ChromaDB|RAG|文档'
```

### 关键日志

```
[INFO] 文件保存成功: uploads/doc_xxx_document.pdf, 大小: 1024000 字节
[INFO] PDF 解析成功，提取文本长度: 5000 字符
[INFO] 文档分块完成: 10 个块
[INFO] 向知识库 kb_xxx 添加了 10 个文档块
[INFO] 文档上传成功: document.pdf (ID: doc_xxx), 共 10 个块
```

---

## 技术细节

### ChromaDB Collection 命名

```python
# 每个知识库对应一个 Collection
collection_name = f"kb_{kb_id}"

# 例如
kb_001 -> collection: kb_kb001
kb_002 -> collection: kb_kb002
```

### 文档块 ID 格式

```python
# 格式: {document_id}_chunk_{index}
chunk_id = f"{doc_id}_chunk_{0}"

# 例如
doc_abc123_chunk_0
doc_abc123_chunk_1
doc_abc123_chunk_2
```

### 元数据结构

```python
{
    'document_id': 'doc_xxx',
    'document_name': 'document.pdf',
    'kb_id': 'kb_xxx',
    'chunk_index': 0,
    'chunk_total': 10,
    'source': 'document.pdf'
}
```

---

## 最佳实践

1. **文档质量**: 确保上传的文档内容清晰、格式规范
2. **分块大小**: 根据文档类型调整分块大小
3. **定期备份**: 定期备份 `chroma_db` 和 `uploads` 目录
4. **监控日志**: 关注文档上传和检索的日志信息
5. **性能优化**: 根据实际使用情况调整配置参数

---

## 相关文档

- [Ollama 配置说明](./Ollama配置说明.md)
- [快速开始指南](./快速开始.md)
- [ChromaDB 官方文档](https://docs.trychroma.com/)

---

**配置完成，系统已就绪！** 🎉

