# """
# 大语言模型服务
# 支持多种LLM提供商，实现RAG问答功能
# """
# # RAG and AI services @start
# import os
# import logging
# import time
# from typing import List, Dict, Any, Optional
# from django.conf import settings

# # LLM相关库
# import openai
# from langchain.schema import HumanMessage, SystemMessage, AIMessage

# logger = logging.getLogger(__name__)


# class LLMService:
#     """大语言模型服务类"""
    
#     def __init__(self):
#         """初始化LLM服务"""
#         self.temperature = settings.RAG_SETTINGS['TEMPERATURE']
        
#         # 初始化OpenAI客户端
#         if settings.OPENAI_API_KEY:
#             openai.api_key = settings.OPENAI_API_KEY
#             if settings.OPENAI_API_BASE:
#                 openai.api_base = settings.OPENAI_API_BASE
    
#     def generate_response(self, query: str, context: str, 
#                          conversation_history: List[Dict] = None,
#                          model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
#         """
#         生成AI回答
        
#         Args:
#             query: 用户问题
#             context: 检索到的上下文
#             conversation_history: 对话历史
#             model: 使用的模型
            
#         Returns:
#             Dict: 包含回答和元数据的字典
#         """
#         start_time = time.time()
        
#         try:
#             # 构建系统提示
#             system_prompt = self._build_system_prompt()
            
#             # 构建用户提示
#             user_prompt = self._build_user_prompt(query, context)
            
#             # 构建消息列表
#             messages = [{"role": "system", "content": system_prompt}]
            
#             # 添加对话历史（如果有）
#             if conversation_history:
#                 for msg in conversation_history[-6:]:  # 只保留最近6条消息
#                     messages.append({
#                         "role": msg["role"],
#                         "content": msg["content"]
#                     })
            
#             # 添加当前问题
#             messages.append({"role": "user", "content": user_prompt})
            
#             # 调用OpenAI API
#             response = self._call_openai(messages, model)
            
#             # 计算响应时间
#             response_time = time.time() - start_time
            
#             # 估算token使用量
#             token_count = self._estimate_tokens(messages, response)
            
#             return {
#                 'response': response,
#                 'response_time': response_time,
#                 'token_count': token_count,
#                 'model': model,
#                 'success': True
#             }
            
#         except Exception as e:
#             logger.error(f"生成回答失败: {str(e)}")
#             return {
#                 'response': "抱歉，我暂时无法回答您的问题。请稍后再试。",
#                 'response_time': time.time() - start_time,
#                 'token_count': 0,
#                 'model': model,
#                 'success': False,
#                 'error': str(e)
#             }
    
#     def _build_system_prompt(self) -> str:
#         """构建系统提示"""
#         return """你是一个专业的HR技术助手，专门帮助员工解答技术文档、公司政策和工作流程相关的问题。

# 请遵循以下原则：
# 1. 基于提供的上下文信息回答问题，确保准确性
# 2. 如果上下文中没有相关信息，请明确说明并建议联系相关部门
# 3. 回答要简洁明了，结构清晰
# 4. 使用友好、专业的语气
# 5. 如果涉及敏感信息，请提醒用户注意保密
# 6. 可以提供相关的操作步骤或建议

# 回答格式：
# - 直接回答问题
# - 如有必要，提供详细步骤
# - 标注信息来源（如果来自特定文档）
# - 提供相关建议或注意事项"""
    
#     def _build_user_prompt(self, query: str, context: str) -> str:
#         """构建用户提示"""
#         prompt = f"""基于以下上下文信息，请回答用户的问题：

# 上下文信息：
# {context}

# 用户问题：{query}

# 请基于上述上下文信息提供准确、有用的回答。如果上下文中没有足够的信息来回答问题，请说明这一点。"""
        
#         return prompt
    
#     def _call_openai(self, messages: List[Dict], model: str) -> str:
#         """调用OpenAI API"""
#         try:
#             response = openai.ChatCompletion.create(
#                 model=model,
#                 messages=messages,
#                 temperature=self.temperature,
#                 max_tokens=1000,
#                 top_p=1,
#                 frequency_penalty=0,
#                 presence_penalty=0
#             )
            
#             return response.choices[0].message.content.strip()
            
#         except openai.error.AuthenticationError:
#             logger.error("OpenAI API认证失败")
#             raise Exception("AI服务认证失败，请联系管理员")
#         except openai.error.RateLimitError:
#             logger.error("OpenAI API速率限制")
#             raise Exception("AI服务繁忙，请稍后再试")
#         except openai.error.APIError as e:
#             logger.error(f"OpenAI API错误: {e}")
#             raise Exception("AI服务暂时不可用")
#         except Exception as e:
#             logger.error(f"调用OpenAI失败: {e}")
#             raise
    
#     def _estimate_tokens(self, messages: List[Dict], response: str) -> int:
#         """估算token使用量"""
#         try:
#             # 简单估算：中文字符*2 + 英文单词*1.3
#             total_text = ""
#             for msg in messages:
#                 total_text += msg["content"]
#             total_text += response
            
#             # 计算中文字符数
#             chinese_chars = len([c for c in total_text if '\u4e00' <= c <= '\u9fff'])
#             # 计算英文单词数（粗略估算）
#             english_words = len(total_text.split()) - chinese_chars
            
#             return int(chinese_chars * 2 + english_words * 1.3)
            
#         except Exception:
#             return len(total_text) // 4  # 回退估算
    
#     def generate_title_for_session(self, first_message: str) -> str:
#         """
#         为会话生成标题
        
#         Args:
#             first_message: 第一条消息
            
#         Returns:
#             str: 生成的标题
#         """
#         try:
#             # 如果消息太短，直接使用
#             if len(first_message) <= 20:
#                 return first_message
            
#             # 简单的标题生成逻辑
#             # 提取关键词或使用前20个字符
#             title = first_message[:20] + "..."
            
#             # 尝试提取问题的主要内容
#             if "如何" in first_message:
#                 title = "如何" + first_message.split("如何")[1][:15] + "..."
#             elif "什么" in first_message:
#                 title = "什么" + first_message.split("什么")[1][:15] + "..."
#             elif "怎么" in first_message:
#                 title = "怎么" + first_message.split("怎么")[1][:15] + "..."
            
#             return title
            
#         except Exception:
#             return "新会话"
    
#     def format_context_from_documents(self, search_results: Dict[str, Any]) -> str:
#         """
#         从搜索结果格式化上下文
        
#         Args:
#             search_results: 向量搜索结果
            
#         Returns:
#             str: 格式化的上下文
#         """
#         if not search_results['documents']:
#             return "未找到相关文档信息。"
        
#         context_parts = []
        
#         for i, (doc, metadata) in enumerate(zip(
#             search_results['documents'], 
#             search_results['metadatas']
#         )):
#             # 获取文档信息
#             doc_title = metadata.get('title', '未知文档')
#             doc_type = metadata.get('document_type', '未知类型')
            
#             # 格式化文档片段
#             context_part = f"""
# 文档{i+1}：{doc_title} ({doc_type})
# 内容：{doc}
# """
#             context_parts.append(context_part)
        
#         return "\n".join(context_parts)
    
#     def check_service_health(self) -> Dict[str, Any]:
#         """
#         检查服务健康状态
        
#         Returns:
#             Dict: 健康状态信息
#         """
#         health_status = {
#             'openai_configured': bool(settings.OPENAI_API_KEY),
#             'api_base': settings.OPENAI_API_BASE,
#             'temperature': self.temperature,
#             'service_available': False
#         }
        
#         # 测试API连接
#         if health_status['openai_configured']:
#             try:
#                 # 发送一个简单的测试请求
#                 test_response = openai.ChatCompletion.create(
#                     model="gpt-3.5-turbo",
#                     messages=[{"role": "user", "content": "Hello"}],
#                     max_tokens=5
#                 )
#                 health_status['service_available'] = True
#                 health_status['test_response'] = "API连接正常"
#             except Exception as e:
#                 health_status['test_response'] = f"API连接失败: {str(e)}"
        
#         return health_status 
# # RAG and AI services @end