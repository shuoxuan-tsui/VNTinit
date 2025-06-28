# """
# 向量数据库服务
# 使用ChromaDB实现文档的向量化存储和检索
# """

# import os
# import logging
# import chromadb
# from chromadb.config import Settings
# from sentence_transformers import SentenceTransformer
# from typing import List, Dict, Any, Optional
# from django.conf import settings
# import uuid

# logger = logging.getLogger(__name__)


# class VectorService:
#     """向量数据库服务类"""
    
#     def __init__(self):
#         """初始化向量服务"""
#         try:
#             # 初始化ChromaDB客户端
#             self.client = chromadb.PersistentClient(
#                 path=settings.RAG_SETTINGS['VECTOR_DB_PATH'],
#                 settings=Settings(
#                     anonymized_telemetry=False,
#                     allow_reset=True
#                 )
#             )
            
#             # 获取或创建集合
#             self.collection = self.client.get_or_create_collection(
#                 name="hr_knowledge_base",
#                 metadata={"description": "HR技术文档知识库"}
#             )
            
#             # 初始化嵌入模型
#             self.embedding_model = SentenceTransformer(
#                 settings.RAG_SETTINGS['EMBEDDING_MODEL']
#             )
            
#             logger.info("向量服务初始化成功")
            
#         except Exception as e:
#             logger.error(f"向量服务初始化失败: {str(e)}")
#             raise
    
#     def add_document_chunks(self, document_id: str, chunks: List[str], 
#                           metadata: Dict[str, Any]) -> bool:
#         """
#         添加文档分块到向量数据库
        
#         Args:
#             document_id: 文档ID
#             chunks: 文档分块列表
#             metadata: 文档元数据
            
#         Returns:
#             bool: 是否成功
#         """
#         try:
#             # 为每个分块生成唯一ID
#             chunk_ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
            
#             # 为每个分块添加元数据
#             chunk_metadatas = []
#             for i, chunk in enumerate(chunks):
#                 chunk_metadata = metadata.copy()
#                 chunk_metadata.update({
#                     'chunk_index': i,
#                     'chunk_id': chunk_ids[i],
#                     'document_id': document_id,
#                     'chunk_text_length': len(chunk)
#                 })
#                 chunk_metadatas.append(chunk_metadata)
            
#             # 添加到向量数据库
#             self.collection.add(
#                 documents=chunks,
#                 metadatas=chunk_metadatas,
#                 ids=chunk_ids
#             )
            
#             logger.info(f"成功添加文档 {document_id} 的 {len(chunks)} 个分块")
#             return True
            
#         except Exception as e:
#             logger.error(f"添加文档分块失败: {str(e)}")
#             return False
    
#     def search_similar_documents(self, query: str, top_k: int = None, 
#                                filters: Dict[str, Any] = None) -> Dict[str, Any]:
#         """
#         搜索相似文档
        
#         Args:
#             query: 搜索查询
#             top_k: 返回结果数量
#             filters: 过滤条件
            
#         Returns:
#             Dict: 搜索结果
#         """
#         try:
#             if top_k is None:
#                 top_k = settings.RAG_SETTINGS['TOP_K_RESULTS']
            
#             # 构建查询参数
#             query_params = {
#                 'query_texts': [query],
#                 'n_results': top_k
#             }
            
#             # 添加过滤条件
#             if filters:
#                 query_params['where'] = filters
            
#             # 执行搜索
#             results = self.collection.query(**query_params)
            
#             # 格式化结果
#             formatted_results = {
#                 'documents': results['documents'][0] if results['documents'] else [],
#                 'metadatas': results['metadatas'][0] if results['metadatas'] else [],
#                 'distances': results['distances'][0] if results['distances'] else [],
#                 'ids': results['ids'][0] if results['ids'] else []
#             }
            
#             logger.info(f"搜索查询 '{query}' 返回 {len(formatted_results['documents'])} 个结果")
#             return formatted_results
            
#         except Exception as e:
#             logger.error(f"搜索相似文档失败: {str(e)}")
#             return {
#                 'documents': [],
#                 'metadatas': [],
#                 'distances': [],
#                 'ids': []
#             }
    
#     def delete_document(self, document_id: str) -> bool:
#         """
#         删除文档的所有分块
        
#         Args:
#             document_id: 文档ID
            
#         Returns:
#             bool: 是否成功
#         """
#         try:
#             # 查找文档的所有分块
#             results = self.collection.query(
#                 query_texts=[""],
#                 n_results=1000,  # 设置一个较大的数字
#                 where={"document_id": document_id}
#             )
            
#             if results['ids'][0]:
#                 # 删除所有分块
#                 self.collection.delete(ids=results['ids'][0])
#                 logger.info(f"成功删除文档 {document_id} 的所有分块")
            
#             return True
            
#         except Exception as e:
#             logger.error(f"删除文档失败: {str(e)}")
#             return False
    
#     def get_collection_stats(self) -> Dict[str, Any]:
#         """
#         获取集合统计信息
        
#         Returns:
#             Dict: 统计信息
#         """
#         try:
#             count = self.collection.count()
#             return {
#                 'total_chunks': count,
#                 'collection_name': self.collection.name,
#                 'embedding_model': settings.RAG_SETTINGS['EMBEDDING_MODEL']
#             }
#         except Exception as e:
#             logger.error(f"获取集合统计失败: {str(e)}")
#             return {'total_chunks': 0}
    
#     def update_document_chunks(self, document_id: str, chunks: List[str], 
#                              metadata: Dict[str, Any]) -> bool:
#         """
#         更新文档分块
        
#         Args:
#             document_id: 文档ID
#             chunks: 新的文档分块列表
#             metadata: 文档元数据
            
#         Returns:
#             bool: 是否成功
#         """
#         try:
#             # 先删除旧的分块
#             self.delete_document(document_id)
            
#             # 添加新的分块
#             return self.add_document_chunks(document_id, chunks, metadata)
            
#         except Exception as e:
#             logger.error(f"更新文档分块失败: {str(e)}")
#             return False
    
#     def reset_collection(self) -> bool:
#         """
#         重置集合（谨慎使用）
        
#         Returns:
#             bool: 是否成功
#         """
#         try:
#             self.client.delete_collection(name="hr_knowledge_base")
#             self.collection = self.client.create_collection(
#                 name="hr_knowledge_base",
#                 metadata={"description": "HR技术文档知识库"}
#             )
#             logger.warning("向量数据库集合已重置")
#             return True
            
#         except Exception as e:
#             logger.error(f"重置集合失败: {str(e)}")
#             return False 