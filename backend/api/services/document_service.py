# """
# RAG and AI services
# 文档处理服务
# 负责文档的解析、分块和索引
# """
# # RAG and AI services @start
# import os
# import logging
# import re
# import magic
# from typing import List, Dict, Any, Tuple
# from django.conf import settings
# from django.core.files.uploadedfile import UploadedFile

# # 文档解析库
# import PyPDF2
# from docx import Document
# import tiktoken

# logger = logging.getLogger(__name__)


# class DocumentProcessor:
#     """文档处理器类"""
    
#     def __init__(self):
#         """初始化文档处理器"""
#         self.chunk_size = settings.RAG_SETTINGS['CHUNK_SIZE']
#         self.chunk_overlap = settings.RAG_SETTINGS['CHUNK_OVERLAP']
        
#         # 初始化tiktoken编码器（用于计算token数量）
#         try:
#             self.encoding = tiktoken.get_encoding("cl100k_base")
#         except Exception as e:
#             logger.warning(f"tiktoken初始化失败: {e}")
#             self.encoding = None
    
#     def extract_text_from_file(self, file_path: str, file_type: str = None) -> str:
#         """
#         从文件中提取文本
        
#         Args:
#             file_path: 文件路径
#             file_type: 文件类型（可选）
            
#         Returns:
#             str: 提取的文本内容
#         """
#         try:
#             # 自动检测文件类型
#             if not file_type:
#                 file_type = self._detect_file_type(file_path)
            
#             # 根据文件类型选择处理方法
#             if file_type == 'pdf':
#                 return self._extract_from_pdf(file_path)
#             elif file_type == 'docx':
#                 return self._extract_from_docx(file_path)
#             elif file_type in ['txt', 'md']:
#                 return self._extract_from_text(file_path)
#             else:
#                 raise ValueError(f"不支持的文件类型: {file_type}")
                
#         except Exception as e:
#             logger.error(f"文本提取失败 {file_path}: {str(e)}")
#             raise
    
#     def _detect_file_type(self, file_path: str) -> str:
#         """检测文件类型"""
#         try:
#             # 使用python-magic检测MIME类型
#             mime_type = magic.from_file(file_path, mime=True)
            
#             if 'pdf' in mime_type:
#                 return 'pdf'
#             elif 'word' in mime_type or 'officedocument' in mime_type:
#                 return 'docx'
#             elif 'text' in mime_type:
#                 # 根据扩展名进一步判断
#                 ext = os.path.splitext(file_path)[1].lower()
#                 if ext == '.md':
#                     return 'md'
#                 else:
#                     return 'txt'
#             else:
#                 # 回退到扩展名检测
#                 ext = os.path.splitext(file_path)[1].lower()
#                 return ext.lstrip('.')
                
#         except Exception as e:
#             logger.warning(f"文件类型检测失败: {e}")
#             # 回退到扩展名
#             ext = os.path.splitext(file_path)[1].lower()
#             return ext.lstrip('.')
    
#     def _extract_from_pdf(self, file_path: str) -> str:
#         """从PDF文件提取文本"""
#         text = ""
#         try:
#             with open(file_path, 'rb') as file:
#                 pdf_reader = PyPDF2.PdfReader(file)
#                 for page in pdf_reader.pages:
#                     text += page.extract_text() + "\n"
#         except Exception as e:
#             logger.error(f"PDF文本提取失败: {e}")
#             raise
        
#         return self._clean_text(text)
    
#     def _extract_from_docx(self, file_path: str) -> str:
#         """从DOCX文件提取文本"""
#         try:
#             doc = Document(file_path)
#             text = ""
#             for paragraph in doc.paragraphs:
#                 text += paragraph.text + "\n"
#         except Exception as e:
#             logger.error(f"DOCX文本提取失败: {e}")
#             raise
        
#         return self._clean_text(text)
    
#     def _extract_from_text(self, file_path: str) -> str:
#         """从文本文件提取内容"""
#         try:
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 text = file.read()
#         except UnicodeDecodeError:
#             # 尝试其他编码
#             try:
#                 with open(file_path, 'r', encoding='gbk') as file:
#                     text = file.read()
#             except UnicodeDecodeError:
#                 with open(file_path, 'r', encoding='latin-1') as file:
#                     text = file.read()
#         except Exception as e:
#             logger.error(f"文本文件读取失败: {e}")
#             raise
        
#         return self._clean_text(text)
    
#     def _clean_text(self, text: str) -> str:
#         """清理文本内容"""
#         # 移除多余的空白字符
#         text = re.sub(r'\s+', ' ', text)
#         # 移除特殊字符（保留中文、英文、数字和常用标点）
#         text = re.sub(r'[^\u4e00-\u9fff\w\s.,!?;:()[\]{}""''—\-]', '', text)
#         # 移除过短的行
#         lines = text.split('\n')
#         cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 3]
        
#         return '\n'.join(cleaned_lines)
    
#     def split_text_into_chunks(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
#         """
#         将文本分割成块
        
#         Args:
#             text: 输入文本
#             metadata: 元数据
            
#         Returns:
#             List[Dict]: 文本块列表，每个包含text和metadata
#         """
#         if not text or len(text.strip()) == 0:
#             return []
        
#         chunks = []
        
#         # 按段落分割
#         paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
#         current_chunk = ""
#         current_length = 0
        
#         for paragraph in paragraphs:
#             paragraph_length = len(paragraph)
            
#             # 如果当前块加上新段落超过限制
#             if current_length + paragraph_length > self.chunk_size and current_chunk:
#                 # 保存当前块
#                 chunk_metadata = metadata.copy() if metadata else {}
#                 chunk_metadata.update({
#                     'chunk_length': len(current_chunk),
#                     'token_count': self._count_tokens(current_chunk)
#                 })
                
#                 chunks.append({
#                     'text': current_chunk.strip(),
#                     'metadata': chunk_metadata
#                 })
                
#                 # 开始新块（保留重叠部分）
#                 if self.chunk_overlap > 0:
#                     overlap_text = current_chunk[-self.chunk_overlap:]
#                     current_chunk = overlap_text + " " + paragraph
#                     current_length = len(current_chunk)
#                 else:
#                     current_chunk = paragraph
#                     current_length = paragraph_length
#             else:
#                 # 添加到当前块
#                 if current_chunk:
#                     current_chunk += "\n\n" + paragraph
#                 else:
#                     current_chunk = paragraph
#                 current_length += paragraph_length
        
#         # 添加最后一个块
#         if current_chunk.strip():
#             chunk_metadata = metadata.copy() if metadata else {}
#             chunk_metadata.update({
#                 'chunk_length': len(current_chunk),
#                 'token_count': self._count_tokens(current_chunk)
#             })
            
#             chunks.append({
#                 'text': current_chunk.strip(),
#                 'metadata': chunk_metadata
#             })
        
#         logger.info(f"文本分割完成，共生成 {len(chunks)} 个块")
#         return chunks
    
#     def _count_tokens(self, text: str) -> int:
#         """计算文本的token数量"""
#         if self.encoding:
#             try:
#                 return len(self.encoding.encode(text))
#             except Exception:
#                 pass
        
#         # 回退到字符数估算（中文字符按2个token计算）
#         chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
#         other_chars = len(text) - chinese_chars
#         return chinese_chars * 2 + other_chars // 4
    
#     def validate_file(self, uploaded_file: UploadedFile) -> Tuple[bool, str]:
#         """
#         验证上传的文件
        
#         Args:
#             uploaded_file: 上传的文件
            
#         Returns:
#             Tuple[bool, str]: (是否有效, 错误信息)
#         """
#         try:
#             # 检查文件大小
#             if uploaded_file.size > settings.MAX_DOCUMENT_SIZE:
#                 return False, f"文件大小超过限制 ({settings.MAX_DOCUMENT_SIZE // (1024*1024)}MB)"
            
#             # 检查文件类型
#             file_ext = os.path.splitext(uploaded_file.name)[1].lower()
#             if file_ext not in settings.ALLOWED_DOCUMENT_TYPES:
#                 return False, f"不支持的文件类型: {file_ext}"
            
#             # 检查文件名
#             if not uploaded_file.name or len(uploaded_file.name) > 200:
#                 return False, "文件名无效"
            
#             return True, ""
            
#         except Exception as e:
#             return False, f"文件验证失败: {str(e)}"
    
#     def save_uploaded_file(self, uploaded_file: UploadedFile, document_id: str) -> str:
#         """
#         保存上传的文件
        
#         Args:
#             uploaded_file: 上传的文件
#             document_id: 文档ID
            
#         Returns:
#             str: 保存的文件路径
#         """
#         try:
#             # 生成文件路径
#             file_ext = os.path.splitext(uploaded_file.name)[1]
#             filename = f"{document_id}{file_ext}"
#             file_path = os.path.join(settings.DOCUMENT_UPLOAD_PATH, filename)
            
#             # 保存文件
#             with open(file_path, 'wb') as destination:
#                 for chunk in uploaded_file.chunks():
#                     destination.write(chunk)
            
#             logger.info(f"文件保存成功: {file_path}")
#             return file_path
            
#         except Exception as e:
#             logger.error(f"文件保存失败: {str(e)}")
#             raise
    
#     def delete_file(self, file_path: str) -> bool:
#         """
#         删除文件
        
#         Args:
#             file_path: 文件路径
            
#         Returns:
#             bool: 是否成功
#         """
#         try:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#                 logger.info(f"文件删除成功: {file_path}")
#             return True
#         except Exception as e:
#             logger.error(f"文件删除失败: {str(e)}")
#             return False 
# # RAG and AI services @end