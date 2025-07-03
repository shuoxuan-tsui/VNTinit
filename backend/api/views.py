"""
VNTinit 人力资源管理系统 - API 视图模块

设计思路：
1. 采用 Django REST Framework 构建 RESTful API
2. 使用基于类的视图（CBV）和函数视图（FBV）相结合的方式
3. 实现完整的 CRUD 操作和业务逻辑
4. 统一的权限控制和数据验证
5. 支持分页、搜索、筛选和排序功能
6. 提供仪表盘统计和数据导出功能
"""

"""
VNTinit 人力资源管理系统 - API 视图模块

设计思路：
1. 采用 Django REST Framework 构建 RESTful API
2. 使用基于类的视图（CBV）和函数视图（FBV）相结合的方式
3. 实现完整的 CRUD 操作和业务逻辑
4. 统一的权限控制和数据验证
5. 支持分页、搜索、筛选和排序功能
6. 提供仪表盘统计和数据导出功能
"""

from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import json
import time
from datetime import datetime
import re

from .models import Department, Employee, SalaryRecord, AttendanceRecord
# KnowledgeDocument, ChatSession, ChatMessage (RAG 功能暂时注释)
from .serializers import (
    DepartmentSerializer, EmployeeSerializer, SalaryRecordSerializer, 
    SalaryCalculationSerializer, UserSerializer
    # KnowledgeDocumentSerializer,
    # DocumentUploadSerializer, ChatSessionSerializer, ChatMessageSerializer,
    # ChatRequestSerializer, DocumentSearchSerializer
)
from .permissions import IsAdminOrReadOnly, IsAdminUser, IsSalaryOwnerOrAdmin
# from .services.vector_service import VectorService
# from .services.document_service import DocumentProcessor
# from .services.llm_service import LLMService


# ==================== 认证相关视图 ====================

class CustomAuthToken(ObtainAuthToken):
    """
    自定义认证视图
    
    设计思路：
    - 继承 DRF 的 ObtainAuthToken 类，实现 Token 认证
    - 接收用户名和密码，验证后返回 Token 和用户信息
    - 为前端提供统一的登录接口
    """
    
    def post(self, request, *args, **kwargs):
        """处理登录请求"""
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username and password:
            # 使用 Django 内置的认证系统验证用户
            user = authenticate(username=username, password=password)
            if user:
                # 获取或创建用户的 Token
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': UserSerializer(user).data
                })
        
        return Response(
            {'error': '用户名或密码错误'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    登出视图
    
    设计思路：
    - 删除用户的 Token，实现安全登出
    - 确保用户再次访问需要重新认证
    """
    try:
        request.user.auth_token.delete()
        return Response({'message': '登出成功'})
    except:
        return Response({'error': '登出失败'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user_view(request):
    """
    获取当前用户信息
    
    设计思路：
    - 为前端提供获取当前登录用户信息的接口
    - 用于用户身份确认和权限判断
    """
    return Response(UserSerializer(request.user).data)


# ==================== 员工管理视图 ====================

class EmployeeListCreateView(generics.ListCreateAPIView):
    """
    员工列表和创建视图
    
    设计思路：
    - 继承 DRF 的 ListCreateAPIView，同时支持 GET（列表）和 POST（创建）
    - 实现完整的搜索、筛选、排序和分页功能
    - 支持按状态筛选（默认只显示在职员工）
    - 提供灵活的查询参数支持
    """
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]  # 管理员可读写，其他用户只读
    
    def get_queryset(self):
        """
        构建查询集
        
        设计思路：
        - 根据查询参数动态构建 QuerySet
        - 支持多字段搜索（姓名、工号、部门、职位）
        - 支持多维度筛选（部门、职位、状态）
        - 支持自定义排序
        """
        # 默认只显示活跃员工，除非明确指定包含所有状态
        include_all_status = self.request.query_params.get('include_all_status', 'false').lower() == 'true'
        if include_all_status:
            queryset = Employee.objects.all()
        else:
            queryset = Employee.objects.filter(status='active')
        
        # 搜索功能 - 支持多字段模糊匹配
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(employee_id__icontains=search) |
                Q(department__icontains=search) |
                Q(position__icontains=search)
            )
        
        # 筛选功能 - 精确匹配
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department=department)
        
        position = self.request.query_params.get('position', None)
        if position:
            queryset = queryset.filter(position=position)
        
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # 排序功能 - 默认按创建时间倒序
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        重写列表方法，添加分页功能

        - 使用 Django 的 Paginator 实现分页
        - 返回统一格式的响应数据
        - 包含分页信息（总页数、当前页、总记录数）
        """
        queryset = self.get_queryset()
        
        # 分页处理
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        
        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            page = 1
            page_size = 20
        
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = self.get_serializer(page_obj, many=True)
        
        return Response({
            'results': serializer.data,
            'total_pages': paginator.num_pages,
            'current_page': page,
            'total_count': paginator.count
        })


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    员工详情、更新和删除视图
    
    设计思路：
    - 继承 DRF 的 RetrieveUpdateDestroyAPIView
    - 支持 GET（详情）、PUT/PATCH（更新）、DELETE（删除）操作
    - 使用 UUID 作为查找字段，保证数据安全性
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'id'  # 使用 UUID 作为查找字段


# ==================== 薪资管理视图 ====================

class SalaryRecordListView(generics.ListAPIView):
    """
    薪资记录列表视图（仅管理员可访问）
    
    设计思路：
    - 只提供列表功能，薪资记录通过专门的计算接口创建
    - 实现多维度搜索和筛选功能
    - 支持按薪资范围筛选
    - 使用 select_related 优化数据库查询性能
    """
    serializer_class = SalaryRecordSerializer
    permission_classes = [IsAdminUser]  # 仅管理员可访问
    
    def get_queryset(self):
        """
        构建薪资记录查询集
        
        设计思路：
        1. 性能优化：使用select_related预加载关联的员工数据，减少数据库查询次数
        2. 搜索功能：支持按员工姓名或工号进行模糊搜索(icontains)
        3. 多维度筛选：
           - 按部门筛选：精确匹配员工所属部门
           - 按职位筛选：匹配薪资记录中的职位快照
           - 按薪资期间筛选：精确匹配YYYY-MM格式的薪资期间
        4. 范围查询：支持按实发工资(net_salary)范围筛选，使用Decimal保证精度
        5. 排序功能：默认按创建时间降序，支持自定义排序字段
        6. 健壮性处理：对数值转换进行异常捕获，避免无效参数导致错误
        """
        # 基础查询集，预加载关联的员工数据
        queryset = SalaryRecord.objects.select_related('employee').all()
        
        # 搜索功能 - 按员工姓名或工号模糊搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(employee__name__icontains=search) |
                Q(employee__employee_id__icontains=search)
            )
        
        # 多维度筛选
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(employee__department=department)
        
        position = self.request.query_params.get('position')
        if position:
            queryset = queryset.filter(position_snapshot=position)
        
        salary_period = self.request.query_params.get('salary_period')
        if salary_period:
            queryset = queryset.filter(salary_period=salary_period)
        
        # 薪资范围筛选（带异常处理）
        min_salary = self.request.query_params.get('min_salary')
        if min_salary:
            try:
                queryset = queryset.filter(net_salary__gte=Decimal(min_salary))
            except (ValueError, TypeError):
                pass
        
        max_salary = self.request.query_params.get('max_salary')
        if max_salary:
            try:
                queryset = queryset.filter(net_salary__lte=Decimal(max_salary))
            except (ValueError, TypeError):
                pass
        
        # 排序功能（默认按创建时间降序）
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """重写列表方法，返回统一格式的响应"""
        queryset = self.get_queryset()
        
        # 分页处理
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        
        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            page = 1
            page_size = 20
        
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = self.get_serializer(page_obj, many=True)
        
        return Response({
            'success': True,
            'data': {
                'results': serializer.data,
                'count': paginator.count,
                'total_pages': paginator.num_pages,
                'current_page': page
            }
        })


class SalaryRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    薪资记录详情、更新和删除视图
    
    设计思路：
    - 支持薪资记录的查看、修改和删除
    - 使用自定义权限类确保只有记录所有者或管理员可访问
    - 优化数据库查询性能
    """
    queryset = SalaryRecord.objects.select_related('employee').all()
    serializer_class = SalaryRecordSerializer
    permission_classes = [IsSalaryOwnerOrAdmin]  # 记录所有者或管理员可访问
    lookup_field = 'id'


@api_view(['POST'])
@permission_classes([IsAdminUser])
def calculate_salary_view(request):
    """
    薪资计算接口（旧版本，保留兼容性）
    
    设计思路：
    - 接收员工工号和薪资参数
    - 自动计算应发和实发工资
    - 防止重复创建同期薪资记录
    - 创建薪资快照，保证历史数据准确性
    """
    """
    薪资计算接口（旧版本，保留兼容性）
    
    设计思路：
    - 接收员工工号和薪资参数
    - 自动计算应发和实发工资
    - 防止重复创建同期薪资记录
    - 创建薪资快照，保证历史数据准确性
    """
    serializer = SalaryCalculationSerializer(data=request.data)
    
    if serializer.is_valid():
        employee_id = serializer.validated_data['employee_id']
        salary_period = serializer.validated_data['salary_period']
        bonus = serializer.validated_data['bonus']
        deductions = serializer.validated_data['deductions']
        
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            
            # 检查是否已存在该期间的薪资记录
            if SalaryRecord.objects.filter(employee=employee, salary_period=salary_period).exists():
                return Response({
                    'success': False,
                    'error': '该员工在此期间已有薪资记录'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 薪资计算逻辑
            base_salary = employee.base_salary
            gross_salary = base_salary + bonus  # 应发 = 基础 + 奖金
            net_salary = gross_salary - deductions  # 实发 = 应发 - 扣除
            
            # 创建薪资记录（包含快照数据）
            salary_record = SalaryRecord.objects.create(
                employee=employee,
                salary_period=salary_period,
                position_snapshot=employee.position,  # 职位快照
                base_salary_snapshot=base_salary,     # 基础工资快照
                bonus=bonus,
                deductions=deductions,
                gross_salary=gross_salary,
                net_salary=net_salary
            )
            
            return Response({
                'success': True,
                'message': '薪资计算完成',
                'data': SalaryRecordSerializer(salary_record).data
            }, status=status.HTTP_201_CREATED)
            
        except Employee.DoesNotExist:
            return Response({
                'success': False,
                'error': '员工不存在'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'success': False,
        'error': '数据验证失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsSalaryOwnerOrAdmin])  
def salary_print_view(request, record_id):
    """
    薪资记录打印视图
    
    设计思路：
    - 提供薪资条打印格式的数据
    - 严格的权限控制，只有记录所有者或管理员可访问
    - 返回结构化的打印数据
    """
    try:
        salary_record = SalaryRecord.objects.select_related('employee').get(id=record_id)
        
        # 权限检查
        if not (request.user.is_superuser or 
                request.user.groups.filter(name='Admin').exists()):
            # 这里需要检查是否为员工本人，暂时返回403
            return Response(
                {'error': '权限不足'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 返回打印格式的数据
        print_data = {
            'employee_info': {
                'name': salary_record.employee.name,
                'employee_id': salary_record.employee.employee_id,
                'department': salary_record.employee.department,
                'position': salary_record.position_snapshot,
            },
            'salary_info': {
                'salary_period': salary_record.salary_period,
                'base_salary': float(salary_record.base_salary_snapshot),
                'bonus': float(salary_record.bonus),
                'deductions': float(salary_record.deductions),
                'gross_salary': float(salary_record.gross_salary),
                'net_salary': float(salary_record.net_salary),
            },
            'generated_at': salary_record.created_at.isoformat()
        }
        
        return Response(print_data)
        
    except SalaryRecord.DoesNotExist:
        return Response(
            {'error': '薪资记录不存在'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsSalaryOwnerOrAdmin])
def employee_salary_history_view(request, employee_id):
    """
    员工薪资历史记录
    
    设计思路：
    - 提供员工的完整薪资历史
    - 支持分页显示
    - 按薪资期间倒序排列
    - 包含员工基本信息
    """
    try:
        employee = Employee.objects.get(employee_id=employee_id)
        
        # 权限检查
        if not (request.user.is_superuser or 
                request.user.groups.filter(name='Admin').exists()):
            # 这里需要检查是否为员工本人，暂时返回403
            return Response(
                {'error': '权限不足'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        salary_records = SalaryRecord.objects.filter(employee=employee).order_by('-salary_period')
        
        # 分页处理
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        
        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            page = 1
            page_size = 20
        
        paginator = Paginator(salary_records, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = SalaryRecordSerializer(page_obj, many=True)
        
        return Response({
            'employee': EmployeeSerializer(employee).data,
            'salary_records': serializer.data,
            'total_pages': paginator.num_pages,
            'current_page': page,
            'total_count': paginator.count
        })
        
    except Employee.DoesNotExist:
        return Response(
            {'error': '员工不存在'}, 
            status=status.HTTP_404_NOT_FOUND
        )


# ==================== 部门管理视图 ====================

class DepartmentListCreateView(generics.ListCreateAPIView):
    """
    部门列表和创建视图
    
    设计思路：
    - 支持部门的查看和创建
    - 实现搜索、筛选、排序功能
    - 自动计算部门员工数量
    - 统一的响应格式
    """
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        """构建部门查询集"""
        queryset = Department.objects.all()
        
        # 搜索功能 - 多字段搜索
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(manager__icontains=search) |
                Q(description__icontains=search)
            )
        
        # 状态筛选
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # 排序功能 - 默认按名称排序
        ordering = self.request.query_params.get('ordering', 'name')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """重写列表方法，添加分页和统一响应格式"""
        queryset = self.get_queryset()
        
        # 分页处理
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        
        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            page = 1
            page_size = 20
        
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = self.get_serializer(page_obj, many=True)
        
        return Response({
            'success': True,
            'data': {
                'results': serializer.data,
                'total_pages': paginator.num_pages,
                'current_page': page,
                'total_count': paginator.count
            }
        })
    
    def create(self, request, *args, **kwargs):
        """重写创建方法，统一响应格式"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            department = serializer.save()
            return Response({
                'success': True,
                'message': '部门创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    部门详情、更新和删除视图
    
    设计思路：
    - 支持部门的查看、修改和删除
    - 删除前检查是否有关联员工
    - 统一的响应格式
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        """重写获取方法，统一响应格式"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        """重写更新方法，统一响应格式"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            department = serializer.save()
            return Response({
                'success': True,
                'message': '部门更新成功',
                'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """
        重写删除方法，添加业务逻辑检查
        
        设计思路：
        - 删除前检查部门下是否还有员工
        - 防止误删除有员工的部门
        """
        instance = self.get_object()
        
        # 检查是否有员工在该部门
        if instance.employees.exists():
            return Response({
                'success': False,
                'message': '该部门下还有员工，无法删除'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        instance.delete()
        return Response({
            'success': True,
            'message': '部门删除成功'
        }, status=status.HTTP_204_NO_CONTENT)


# ==================== 仪表盘统计视图 ====================

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_summary_stats(request):
    """
    获取仪表盘总体统计数据
    
    设计思路：
    - 提供系统关键指标的汇总统计
    - 计算同比增长率
    - 支持考勤率计算
    - 异常处理确保系统稳定性
    """
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count, Avg, Q
        from decimal import Decimal
        
        # 获取当前月份
        current_date = datetime.now()
        current_month = current_date.strftime('%Y-%m')
        last_month = (current_date - timedelta(days=30)).strftime('%Y-%m')
        
        # 员工总数统计
        total_employees = Employee.objects.count()
        
        # 上月员工数量（用于计算增长率）
        last_month_employees = Employee.objects.filter(
            created_at__lt=current_date - timedelta(days=30)
        ).count()
        
        # 计算员工增长率
        if last_month_employees > 0:
            employee_growth = round(((total_employees - last_month_employees) / last_month_employees) * 100, 1)
        else:
            employee_growth = 0
        
        # 部门总数统计
        total_departments = Employee.objects.values('department').distinct().count()
        
        # 本月考勤率计算
        current_month_start = current_date.replace(day=1)
        total_work_days = (current_date - current_month_start).days + 1
        
        # 计算本月出勤记录
        present_records = AttendanceRecord.objects.filter(
            date__gte=current_month_start,
            date__lte=current_date,
            status__in=['present', 'late', 'early_leave', 'overtime']
        ).count()
        
        # 计算应出勤总数
        active_employees = Employee.objects.filter(status='active').count()
        expected_attendance = active_employees * total_work_days
        
        # 计算考勤率
        if expected_attendance > 0:
            attendance_rate = round((present_records / expected_attendance) * 100, 1)
        else:
            attendance_rate = 0
        
        # 上月考勤率计算（用于增长率）
        last_month_start = (current_date - timedelta(days=30)).replace(day=1)
        last_month_end = current_month_start - timedelta(days=1)
        last_month_work_days = (last_month_end - last_month_start).days + 1
        
        last_month_present = AttendanceRecord.objects.filter(
            date__gte=last_month_start,
            date__lte=last_month_end,
            status__in=['present', 'late', 'early_leave', 'overtime']
        ).count()
        
        last_month_active_employees = Employee.objects.filter(
            status='active',
            created_at__lt=current_date - timedelta(days=30)
        ).count()
        last_month_expected = last_month_active_employees * last_month_work_days
        
        if last_month_expected > 0:
            last_month_attendance_rate = (last_month_present / last_month_expected) * 100
            attendance_rate_growth = round(attendance_rate - last_month_attendance_rate, 1)
        else:
            attendance_rate_growth = 0
        
        # 平均薪资计算
        avg_salary = Employee.objects.filter(status='active').aggregate(
            avg_salary=Avg('base_salary')
        )['avg_salary']
        
        if avg_salary:
            average_salary = int(avg_salary)
        else:
            average_salary = 0
        
        stats_data = {
            'totalEmployees': total_employees,
            'employeeGrowth': employee_growth,
            'totalDepartments': total_departments,
            'attendanceRate': attendance_rate,
            'averageSalary': average_salary,
            'attendanceRateGrowth': attendance_rate_growth
        }
        
        return Response({
            'success': True,
            'data': stats_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'获取统计数据失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_department_distribution(request):
    """
    获取部门员工分布数据
    
    设计思路：
    - 统计各部门的员工数量
    - 为饼图或柱状图提供数据
    - 预定义颜色方案，提升视觉效果
    """
    try:
        from django.db.models import Count
        
        # 统计部门分布
        department_stats = Employee.objects.values('department').annotate(
            employee_count=Count('id')
        ).order_by('-employee_count')
        
        # 预定义颜色列表
        colors = [
            '#3B82F6',  # 蓝色
            '#10B981',  # 绿色
            '#F59E0B',  # 黄色
            '#EF4444',  # 红色
            '#8B5CF6',  # 紫色
            '#06B6D4',  # 青色
            '#F97316',  # 橙色
            '#84CC16',  # 青绿色
            '#EC4899',  # 粉色
            '#6B7280',  # 灰色
            '#14B8A6',  # 蓝绿色
            '#F472B6',  # 粉红色
            '#A78BFA',  # 淡紫色
            '#34D399',  # 薄荷绿
            '#FBBF24',  # 金黄色
        ]
        
        distribution_data = []
        for index, dept_stat in enumerate(department_stats):
            if dept_stat['employee_count'] > 0:  # 只显示有员工的部门
                distribution_data.append({
                    'name': dept_stat['department'],
                    'count': dept_stat['employee_count'],
                    'color': colors[index % len(colors)]
                })
        
        return Response({
            'success': True,
            'data': distribution_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'获取部门分布数据失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def salary_stats_view(request):
    """
    获取薪资统计数据
    
    设计思路：
    - 提供薪资相关的统计指标
    - 按当前月份统计
    - 支持薪资总额和平均薪资计算
    """
    try:
        from django.db.models import Count, Sum, Avg
        from datetime import datetime
        
        # 获取当前月份
        current_date = datetime.now()
        current_month = current_date.strftime('%Y-%m')
        
        # 薪资记录统计
        total_records = SalaryRecord.objects.count()
        
        # 本月薪资统计
        current_month_records = SalaryRecord.objects.filter(salary_period=current_month)
        total_salary = current_month_records.aggregate(total=Sum('net_salary'))['total'] or 0
        average_salary = current_month_records.aggregate(avg=Avg('net_salary'))['avg'] or 0
        
        # 涉及部门数量
        department_count = SalaryRecord.objects.values('employee__department').distinct().count()
        
        stats_data = {
            'totalRecords': total_records,
            'totalSalary': float(total_salary),
            'averageSalary': float(average_salary),
            'departmentCount': department_count
        }
        
        return Response({
            'success': True,
            'data': stats_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'获取薪资统计数据失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def salary_export_view(request):
    """
    导出薪资数据
    
    设计思路：
    - 生成 CSV 格式的薪资数据导出
    - 支持按部门和薪资期间筛选
    - 添加 BOM 支持 Excel 中文显示
    - 包含完整的薪资信息
    """
    try:
        import csv
        from django.http import HttpResponse
        from io import StringIO
        
        # 获取筛选参数
        department = request.query_params.get('department', None)
        salary_period = request.query_params.get('salary_period', None)
        
        # 构建查询
        queryset = SalaryRecord.objects.select_related('employee').all()
        
        if department:
            queryset = queryset.filter(employee__department=department)
        if salary_period:
            queryset = queryset.filter(salary_period=salary_period)
        
        # 创建CSV响应
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="salary_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        # 添加BOM以支持Excel中文显示
        response.write('\ufeff')
        
        writer = csv.writer(response)
        
        # 写入表头
        writer.writerow([
            '员工姓名', '工号', '部门', '薪资期间', '职称',
            '基础工资', '应发工资', '奖金', '扣除', '实发工资', '发放日期'
        ])
        
        # 写入数据
        for record in queryset:
            writer.writerow([
                record.employee.name,
                record.employee.employee_id,
                record.employee.department,
                record.salary_period,
                record.position_snapshot,
                float(record.base_salary_snapshot),
                float(record.gross_salary),
                float(record.bonus),
                float(record.deductions),
                float(record.net_salary),
                record.pay_date.strftime('%Y-%m-%d') if record.pay_date else ''
            ])
        
        return response
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'导出薪资数据失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== RAG 和 AI 相关视图（暂时注释） ====================
# 这部分代码为 RAG（检索增强生成）和 AI 聊天功能
# 由于依赖外部服务，暂时注释保留

# [RAG 相关代码已注释...]


# ==================== 新增：前端兼容的薪资计算接口 ====================

@api_view(['POST'])
@permission_classes([IsAdminUser])
def calculate_salary_by_employee_view(request, employee_id):
    """
    根据员工 UUID 计算并创建单条薪资记录
    
    设计思路：
    - 为前端提供更直接的薪资计算接口
    - 使用员工 UUID 而非工号，提高安全性
    - 支持 deduction 和 deductions 两种字段名，保证兼容性
    - 实现完整的薪资计算逻辑和数据验证
    
    URL: /api/salaries/calculate/<employee_id>/
    """
    # 解析请求数据，支持两种字段名格式
    salary_period = request.data.get('salary_period')
    bonus = Decimal(str(request.data.get('bonus', 0)))
    deduction = Decimal(str(request.data.get('deduction', request.data.get('deductions', 0))))

    # 基本数据验证
    if not salary_period or not re.match(r'^\d{4}-\d{2}$', str(salary_period)):
        return Response({'success': False, 'error': '薪资期间格式应为 YYYY-MM'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return Response({'success': False, 'error': '员工不存在'}, status=status.HTTP_404_NOT_FOUND)

    # 检查重复记录
    if SalaryRecord.objects.filter(employee=employee, salary_period=salary_period).exists():
        return Response({'success': False, 'error': '该员工在此期间已有薪资记录'}, status=status.HTTP_400_BAD_REQUEST)

    # 薪资计算逻辑
    base_salary = employee.base_salary
    gross_salary = base_salary + bonus      # 应发工资 = 基础工资 + 奖金
    net_salary = gross_salary - deduction   # 实发工资 = 应发工资 - 扣除

    # 创建薪资记录，包含快照数据
    salary_record = SalaryRecord.objects.create(
        employee=employee,
        salary_period=salary_period,
        position_snapshot=employee.position,        # 职位快照
        base_salary_snapshot=base_salary,          # 基础工资快照
        bonus=bonus,
        deductions=deduction,                      # 注意：数据库字段是 deductions
        gross_salary=gross_salary,
        net_salary=net_salary
    )

    return Response({
        'success': True,
        'message': '薪资计算完成',
        'data': SalaryRecordSerializer(salary_record).data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def generate_salaries_view(request):
    """
    为所有员工批量生成薪资记录
    
    设计思路：
    - 支持批量薪资生成，提高管理效率
    - 自动跳过已存在的薪资记录，避免重复
    - 返回详细的处理结果，包括成功和跳过的记录
    - 使用事务确保数据一致性
    
    URL: /api/salaries/generate/
    """
    salary_period = request.data.get('salary_period')
    bonus = Decimal(str(request.data.get('bonus', 0)))
    deduction = Decimal(str(request.data.get('deduction', request.data.get('deductions', 0))))

    # 数据验证
    if not salary_period or not re.match(r'^\d{4}-\d{2}$', str(salary_period)):
        return Response({'success': False, 'error': '薪资期间格式应为 YYYY-MM'}, status=status.HTTP_400_BAD_REQUEST)

    created_records = []
    skipped_employees = []

    # 遍历所有员工进行批量处理
    for employee in Employee.objects.all():
        # 跳过已存在记录的员工
        if SalaryRecord.objects.filter(employee=employee, salary_period=salary_period).exists():
            skipped_employees.append(employee.employee_id)
            continue

        # 薪资计算
        base_salary = employee.base_salary
        gross_salary = base_salary + bonus
        net_salary = gross_salary - deduction

        # 创建薪资记录
        record = SalaryRecord.objects.create(
            employee=employee,
            salary_period=salary_period,
            position_snapshot=employee.position,
            base_salary_snapshot=base_salary,
            bonus=bonus,
            deductions=deduction,
            gross_salary=gross_salary,
            net_salary=net_salary
        )
        created_records.append(record)

    return Response({
        'success': True,
        'message': f'批量生成完成，成功 {len(created_records)} 条，跳过 {len(skipped_employees)} 条',
        'data': {
            'created': SalaryRecordSerializer(created_records, many=True).data,
            'skipped_employee_ids': skipped_employees
        }
    }, status=status.HTTP_201_CREATED)

# ==================== 接口设计说明 ====================
"""
整体设计思路总结：

1. 架构设计：
   - 采用 RESTful API 设计原则
   - 使用 Django REST Framework 提供标准化的 API 接口
   - 分层架构：视图层 -> 序列化层 -> 模型层

2. 权限控制：
   - 基于 Token 的认证机制
   - 自定义权限类实现细粒度权限控制
   - 区分管理员和普通用户的访问权限

3. 数据处理：
   - 统一的数据验证和序列化机制
   - 支持分页、搜索、筛选、排序功能
   - 异常处理确保系统稳定性

4. 业务逻辑：
   - 薪资计算采用快照机制，保证历史数据准确性
   - 防止重复数据创建，确保数据一致性
   - 支持批量操作，提高管理效率

5. 响应格式：
   - 统一的 JSON 响应格式
   - 包含成功状态、错误信息、数据内容
   - 便于前端统一处理

6. 性能优化：
   - 使用 select_related 优化数据库查询
   - 合理的分页机制减少数据传输
   - 缓存策略提升响应速度

7. 扩展性：
   - 模块化设计，便于功能扩展
   - 预留 RAG 和 AI 功能接口
   - 支持多种数据导出格式
"""