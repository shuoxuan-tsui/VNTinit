from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

from .serializers import UserSerializer


class LoginView(APIView):
    """用户登录视图"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """处理用户登录请求
        
        Args:
            request: 包含用户名和密码的请求对象
            
        Returns:
            Response: 包含以下可能的响应:
                - 400: 用户名或密码为空
                - 401: 认证失败(用户名/密码错误或账户禁用)
                - 200: 登录成功(返回token和用户信息)
        """
        # 从请求中获取用户名和密码
        username = request.data.get('username')
        password = request.data.get('password')
        
        # 验证用户名和密码是否为空
        if not username or not password:
            return Response({
                'success': False,
                'message': '用户名和密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 使用Django的authenticate方法验证用户凭证
        user = authenticate(username=username, password=password)
        
        if user:
            # 检查用户账户是否激活
            if user.is_active:
                # 获取或创建用户的认证token
                token, created = Token.objects.get_or_create(user=user)
                # 返回成功响应，包含token和用户序列化数据
                return Response({
                    'success': True,
                    'message': '登录成功',
                    'data': {
                        'token': token.key,  # 认证token
                        'user': UserSerializer(user).data  # 用户信息
                    }
                })
            else:
                # 账户被禁用的情况
                return Response({
                    'success': False,
                    'message': '账户已被禁用'
                }, status=status.HTTP_401_UNAUTHORIZED) # 通常HTTP_401_UNAUTHORIZED状态码表示认证失败
        else:
            # 用户名或密码错误的情况
            return Response({
                'success': False,
                'message': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    """
    用户注册视图
    处理用户注册请求，包括输入验证、用户创建和响应返回
    """
    permission_classes = [permissions.AllowAny]  # 允许所有用户访问
    
    def post(self, request):
        """处理用户注册POST请求
        
        Args:
            request: 包含注册信息的请求对象，需要包含username, email和password
            
        Returns:
            Response: 包含以下可能的响应:
                - 400: 输入验证失败(各种格式错误或已存在)
                - 201: 注册成功(返回用户信息)
                - 500: 服务器内部错误
        """
        # 从请求中获取注册信息
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        # 1. 基础验证 - 检查必填字段
        if not username or not email or not password:
            return Response({
                'success': False,
                'message': '用户名、邮箱和密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. 用户名格式验证
        # 2.1 长度验证
        if len(username) < 3:
            return Response({
                'success': False,
                'message': '用户名至少3位'
            }, status=status.HTTP_400_BAD_REQUEST)
        # 2.2 字符集验证
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return Response({
                'success': False,
                'message': '用户名只能包含字母、数字和下划线'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 3. 邮箱格式验证
        try:
            validate_email(email)
        except ValidationError:
            return Response({
                'success': False,
                'message': '请输入有效的邮箱地址'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 4. 密码强度验证
        if len(password) < 6:
            return Response({
                'success': False,
                'message': '密码至少6位'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 5. 唯一性验证
        # 5.1 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return Response({
                'success': False,
                'message': '用户名已存在'
            }, status=status.HTTP_400_BAD_REQUEST)
        # 5.2 检查邮箱是否已存在
        if User.objects.filter(email=email).exists():
            return Response({
                'success': False,
                'message': '邮箱已被注册'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 6. 创建用户(使用事务保证数据一致性)
        try:
            with transaction.atomic():
                # 使用Django的create_user方法创建用户(会自动处理密码哈希)
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                
                # 返回成功响应(201 Created)
                return Response({
                    'success': True,
                    'message': '注册成功',
                    'data': {
                        'user': UserSerializer(user).data  # 序列化用户信息
                    }
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            # 捕获所有异常并返回服务器错误
            return Response({
                'success': False,
                'message': '注册失败，请稍后重试'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    """用户登出视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            # 删除用户的token
            request.user.auth_token.delete()
            return Response({
                'success': True,
                'message': '登出成功'
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': '登出失败'
            }, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    """获取当前用户信息"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'success': True,
            'data': {
                'user': UserSerializer(request.user).data
            }
        })


class ChangePasswordView(APIView):
    """修改密码视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({
                'success': False,
                'message': '旧密码和新密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证旧密码
        if not request.user.check_password(old_password):
            return Response({
                'success': False,
                'message': '旧密码错误'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证新密码强度
        if len(new_password) < 6:
            return Response({
                'success': False,
                'message': '新密码至少6位'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 设置新密码
            request.user.set_password(new_password)
            request.user.save()
            
            # 删除旧token，强制重新登录
            request.user.auth_token.delete()
            
            return Response({
                'success': True,
                'message': '密码修改成功，请重新登录'
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': '密码修改失败'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# api_view 装饰器用于将函数转换为视图函数 并且仅仅允许GET请求
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated]) # 仅允许已认证的用户访问
def check_auth_view(request):
    """检查用户认证状态
    
    返回:
        Response: 包含以下字段的响应:
            - success (bool): 请求是否成功
            - message (str): 状态消息
            - data (dict): 用户数据，包含序列化后的用户信息
    """
    return Response({
        'success': True,
        'message': '已认证',
        'data': {
            'user': UserSerializer(request.user).data
        }
    }) 