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
# KnowledgeDocument, ChatSession, ChatMessage
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


class CustomAuthToken(ObtainAuthToken):
    """自定义认证视图"""
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
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
    """登出视图"""
    try:
        request.user.auth_token.delete()
        return Response({'message': '登出成功'})
    except:
        return Response({'error': '登出失败'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user_view(request):
    """获取当前用户信息"""
    return Response(UserSerializer(request.user).data)


class EmployeeListCreateView(generics.ListCreateAPIView):
    """员工列表和创建视图"""
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        # 默认只显示活跃员工，除非明确指定包含所有状态
        include_all_status = self.request.query_params.get('include_all_status', 'false').lower() == 'true'
        if include_all_status:
            queryset = Employee.objects.all()
        else:
            queryset = Employee.objects.filter(status='active')
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(employee_id__icontains=search) |
                Q(department__icontains=search) |
                Q(position__icontains=search)
            )
        
        # 筛选功能
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department=department)
        
        position = self.request.query_params.get('position', None)
        if position:
            queryset = queryset.filter(position=position)
        
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # 排序功能
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # 分页
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
    """员工详情、更新和删除视图"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'id'


class SalaryRecordListView(generics.ListAPIView):
    """薪资记录列表视图（管理员）"""
    serializer_class = SalaryRecordSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        queryset = SalaryRecord.objects.select_related('employee').all()
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(employee__name__icontains=search) |
                Q(employee__employee_id__icontains=search)
            )
        
        # 筛选功能
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(employee__department=department)
        
        position = self.request.query_params.get('position', None)
        if position:
            queryset = queryset.filter(position_snapshot=position)
        
        salary_period = self.request.query_params.get('salary_period', None)
        if salary_period:
            queryset = queryset.filter(salary_period=salary_period)
        
        min_salary = self.request.query_params.get('min_salary', None)
        if min_salary:
            try:
                queryset = queryset.filter(net_salary__gte=Decimal(min_salary))
            except:
                pass
        
        max_salary = self.request.query_params.get('max_salary', None)
        if max_salary:
            try:
                queryset = queryset.filter(net_salary__lte=Decimal(max_salary))
            except:
                pass
        
        # 排序功能
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # 分页
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
    """薪资记录详情、更新和删除视图"""
    queryset = SalaryRecord.objects.select_related('employee').all()
    serializer_class = SalaryRecordSerializer
    permission_classes = [IsSalaryOwnerOrAdmin]
    lookup_field = 'id'


@api_view(['POST'])
@permission_classes([IsAdminUser])
def calculate_salary_view(request):
    """计算并创建薪资记录"""
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
            
            # 计算薪资
            base_salary = employee.base_salary
            gross_salary = base_salary + bonus
            net_salary = gross_salary - deductions
            
            # 创建薪资记录
            salary_record = SalaryRecord.objects.create(
                employee=employee,
                salary_period=salary_period,
                position_snapshot=employee.position,
                base_salary_snapshot=base_salary,
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

"""
@api_view装饰器是DRF框架的核心装饰器
将普通函数转换为DRF API视图
明确指定视图函数接受的HTTP请求方法（如GET/POST）
将Django的HttpRequest转换为DRF的Request对象
"""
@api_view(['GET'])
# 这是一个DRF权限装饰器，用于限制视图访问权限。
# IsSalaryOwnerOrAdmin是一个自定义权限类
# 它检查请求用户是否是薪资记录的所有者或者是管理员
@permission_classes([IsSalaryOwnerOrAdmin])  
def salary_print_view(request, record_id):
    """薪资记录打印视图"""
    try:
        salary_record = SalaryRecord.objects.select_related('employee').get(id=record_id)
        
        # 检查权限
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
    """员工薪资历史记录"""
    try:
        employee = Employee.objects.get(employee_id=employee_id)
        
        # 检查权限
        if not (request.user.is_superuser or 
                request.user.groups.filter(name='Admin').exists()):
            # 这里需要检查是否为员工本人，暂时返回403
            return Response(
                {'error': '权限不足'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        salary_records = SalaryRecord.objects.filter(employee=employee).order_by('-salary_period')
        
        # 分页
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


# 部门管理视图
class DepartmentListCreateView(generics.ListCreateAPIView):
    """部门列表和创建视图"""
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        queryset = Department.objects.all()
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(manager__icontains=search) |
                Q(description__icontains=search)
            )
        
        # 筛选功能
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # 排序功能
        ordering = self.request.query_params.get('ordering', 'name')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # 分页
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
    """部门详情、更新和删除视图"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_summary_stats(request):
    """获取仪表盘总体统计数据"""
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count, Avg, Q
        from decimal import Decimal
        
        # 获取当前月份
        current_date = datetime.now()
        current_month = current_date.strftime('%Y-%m')
        last_month = (current_date - timedelta(days=30)).strftime('%Y-%m')
        
        # 员工总数（包括所有状态的员工）
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
        
        # 部门总数（包括所有状态的部门）
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
        
        # 计算应出勤总数（在职员工 * 工作日）
        active_employees = Employee.objects.filter(status='active').count()
        expected_attendance = active_employees * total_work_days
        
        # 计算考勤率
        if expected_attendance > 0:
            attendance_rate = round((present_records / expected_attendance) * 100, 1)
        else:
            attendance_rate = 0
        
        # 上月考勤率（用于计算增长）
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
        
        # 平均薪资
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
    """获取部门员工分布数据"""
    try:
        from django.db.models import Count
        
        # 直接从员工表统计部门分布（包括所有状态的员工）
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
    """获取薪资统计数据"""
    try:
        from django.db.models import Count, Sum, Avg
        from datetime import datetime
        
        # 获取当前月份
        current_date = datetime.now()
        current_month = current_date.strftime('%Y-%m')
        
        # 总薪资记录数
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
    """导出薪资数据"""
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

# RAG and AI views @start
# RAG相关视图

# class KnowledgeDocumentListCreateView(generics.ListCreateAPIView):
#     """知识文档列表和创建视图"""
#     serializer_class = KnowledgeDocumentSerializer
#     permission_classes = [IsAdminOrReadOnly]
    
#     def get_queryset(self):
#         queryset = KnowledgeDocument.objects.all()
        
#         # 搜索功能
#         search = self.request.query_params.get('search', None)
#         if search:
#             queryset = queryset.filter(
#                 Q(title__icontains=search) |
#                 Q(description__icontains=search) |
#                 Q(tags__icontains=search)
#             )
        
#         # 筛选功能
#         document_type = self.request.query_params.get('document_type', None)
#         if document_type:
#             queryset = queryset.filter(document_type=document_type)
        
#         department = self.request.query_params.get('department', None)
#         if department:
#             queryset = queryset.filter(department=department)
        
#         status = self.request.query_params.get('status', None)
#         if status:
#             queryset = queryset.filter(status=status)
        
#         # 排序功能
#         ordering = self.request.query_params.get('ordering', '-created_at')
#         if ordering:
#             queryset = queryset.order_by(ordering)
        
#         return queryset
    
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
        
#         # 分页
#         page = request.query_params.get('page', 1)
#         page_size = request.query_params.get('page_size', 20)
        
#         try:
#             page = int(page)
#             page_size = int(page_size)
#         except ValueError:
#             page = 1
#             page_size = 20
        
#         paginator = Paginator(queryset, page_size)
#         page_obj = paginator.get_page(page)
        
#         serializer = self.get_serializer(page_obj, many=True)
        
#         return Response({
#             'results': serializer.data,
#             'total_pages': paginator.num_pages,
#             'current_page': page,
#             'total_count': paginator.count
#         })


# class KnowledgeDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """知识文档详情、更新和删除视图"""
#     queryset = KnowledgeDocument.objects.all()
#     serializer_class = KnowledgeDocumentSerializer
#     permission_classes = [IsAdminOrReadOnly]
    
#     def destroy(self, request, *args, **kwargs):
#         """删除文档时同时删除向量数据和文件"""
#         document = self.get_object()
        
#         try:
#             # 删除向量数据
#             vector_service = VectorService()
#             vector_service.delete_document(str(document.id))
            
#             # 删除文件
#             document_processor = DocumentProcessor()
#             if document.file_path:
#                 document_processor.delete_file(document.file_path)
            
#             # 删除数据库记录
#             return super().destroy(request, *args, **kwargs)
            
#         except Exception as e:
#             return Response(
#                 {'error': f'删除文档失败: {str(e)}'}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def upload_document_view(request):
#     """文档上传视图"""
#     serializer = DocumentUploadSerializer(data=request.data)
    
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         # 初始化服务
#         document_processor = DocumentProcessor()
#         vector_service = VectorService()
        
#         # 验证文件
#         uploaded_file = serializer.validated_data['file']
#         is_valid, error_msg = document_processor.validate_file(uploaded_file)
#         if not is_valid:
#             return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)
        
#         # 创建文档记录
#         document = KnowledgeDocument.objects.create(
#             title=serializer.validated_data['title'],
#             description=serializer.validated_data.get('description', ''),
#             document_type=serializer.validated_data['document_type'],
#             department_id=serializer.validated_data.get('department'),
#             tags=serializer.validated_data.get('tags', ''),
#             file_name=uploaded_file.name,
#             file_size=uploaded_file.size,
#             uploaded_by=request.user,
#             content='',  # 将在后台处理中填充
#             status='processing'
#         )
        
#         # 保存文件
#         file_path = document_processor.save_uploaded_file(uploaded_file, str(document.id))
#         document.file_path = file_path
#         document.save()
        
#         # 后台处理文档（提取文本、分块、向量化）
#         try:
#             # 提取文本
#             content = document_processor.extract_text_from_file(file_path)
#             document.content = content
            
#             # 分块
#             metadata = {
#                 'title': document.title,
#                 'document_type': document.document_type,
#                 'department': document.department.name if document.department else None,
#                 'uploaded_by': document.uploaded_by.username,
#                 'file_name': document.file_name
#             }
            
#             chunks = document_processor.split_text_into_chunks(content, metadata)
            
#             # 向量化并存储
#             chunk_texts = [chunk['text'] for chunk in chunks]
#             success = vector_service.add_document_chunks(str(document.id), chunk_texts, metadata)
            
#             if success:
#                 document.status = 'indexed'
#                 document.chunk_count = len(chunks)
#             else:
#                 document.status = 'failed'
            
#             document.save()
            
#         except Exception as e:
#             document.status = 'failed'
#             document.save()
#             return Response(
#                 {'error': f'文档处理失败: {str(e)}'}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
        
#         # 返回结果
#         response_serializer = KnowledgeDocumentSerializer(document)
#         return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
#     except Exception as e:
#         return Response(
#             {'error': f'文档上传失败: {str(e)}'}, 
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )


# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def search_documents_view(request):
#     """文档搜索视图"""
#     serializer = DocumentSearchSerializer(data=request.data)
    
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         query = serializer.validated_data['query']
#         top_k = serializer.validated_data['top_k']
#         document_type = serializer.validated_data.get('document_type')
#         department = serializer.validated_data.get('department')
        
#         # 构建过滤条件
#         filters = {}
#         if document_type:
#             filters['document_type'] = document_type
#         if department:
#             filters['department'] = str(department)
        
#         # 向量搜索
#         vector_service = VectorService()
#         search_results = vector_service.search_similar_documents(
#             query=query,
#             top_k=top_k,
#             filters=filters if filters else None
#         )
        
#         # 格式化结果
#         results = []
#         for i, (doc_text, metadata, distance) in enumerate(zip(
#             search_results['documents'],
#             search_results['metadatas'],
#             search_results['distances']
#         )):
#             results.append({
#                 'rank': i + 1,
#                 'content': doc_text[:500] + '...' if len(doc_text) > 500 else doc_text,
#                 'metadata': metadata,
#                 'similarity_score': 1 - distance,  # 转换为相似度分数
#                 'document_id': metadata.get('document_id'),
#                 'title': metadata.get('title'),
#                 'document_type': metadata.get('document_type')
#             })
        
#         return Response({
#             'query': query,
#             'total_results': len(results),
#             'results': results
#         })
        
#     except Exception as e:
#         return Response(
#             {'error': f'搜索失败: {str(e)}'}, 
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )


# class ChatSessionListCreateView(generics.ListCreateAPIView):
#     """聊天会话列表和创建视图"""
#     serializer_class = ChatSessionSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         return ChatSession.objects.filter(user=self.request.user).order_by('-updated_at')
    
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class ChatSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """聊天会话详情、更新和删除视图"""
#     serializer_class = ChatSessionSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         return ChatSession.objects.filter(user=self.request.user)


# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def chat_session_messages_view(request, session_id):
#     """获取会话消息列表"""
#     try:
#         session = ChatSession.objects.get(id=session_id, user=request.user)
#         messages = session.messages.all().order_by('created_at')
#         serializer = ChatMessageSerializer(messages, many=True)
        
#         return Response({
#             'session_id': str(session.id),
#             'session_title': session.title,
#             'messages': serializer.data
#         })
        
#     except ChatSession.DoesNotExist:
#         return Response(
#             {'error': '会话不存在'}, 
#             status=status.HTTP_404_NOT_FOUND
#         )


# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def chat_view(request):
#     """RAG聊天视图"""
#     serializer = ChatRequestSerializer(data=request.data)
    
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         message = serializer.validated_data['message']
#         session_id = serializer.validated_data.get('session_id')
#         model = serializer.validated_data.get('model', 'gpt-3.5-turbo')
        
#         # 获取或创建会话
#         if session_id:
#             try:
#                 session = ChatSession.objects.get(id=session_id, user=request.user)
#             except ChatSession.DoesNotExist:
#                 return Response(
#                     {'error': '会话不存在'}, 
#                     status=status.HTTP_404_NOT_FOUND
#                 )
#         else:
#             # 创建新会话
#             llm_service = LLMService()
#             title = llm_service.generate_title_for_session(message)
#             session = ChatSession.objects.create(
#                 user=request.user,
#                 title=title
#             )
        
#         # 保存用户消息
#         user_message = ChatMessage.objects.create(
#             session=session,
#             role='user',
#             content=message
#         )
        
#         # 初始化服务
#         vector_service = VectorService()
#         llm_service = LLMService()
        
#         start_time = time.time()
        
#         # 检索相关文档
#         search_results = vector_service.search_similar_documents(query=message)
        
#         # 格式化上下文
#         context = llm_service.format_context_from_documents(search_results)
        
#         # 获取对话历史
#         conversation_history = []
#         recent_messages = session.messages.filter(
#             created_at__lt=user_message.created_at
#         ).order_by('-created_at')[:6]
        
#         for msg in reversed(recent_messages):
#             conversation_history.append({
#                 'role': msg.role,
#                 'content': msg.content
#             })
        
#         # 生成回答
#         llm_response = llm_service.generate_response(
#             query=message,
#             context=context,
#             conversation_history=conversation_history,
#             model=model
#         )
        
#         # 准备元数据
#         metadata = {
#             'search_results_count': len(search_results['documents']),
#             'context_length': len(context),
#             'model': model,
#             'referenced_documents': []
#         }
        
#         # 添加引用文档信息
#         for metadata_item in search_results['metadatas']:
#             if metadata_item:
#                 metadata['referenced_documents'].append({
#                     'title': metadata_item.get('title'),
#                     'document_type': metadata_item.get('document_type'),
#                     'document_id': metadata_item.get('document_id')
#                 })
        
#         # 保存助手回复
#         assistant_message = ChatMessage.objects.create(
#             session=session,
#             role='assistant',
#             content=llm_response['response'],
#             metadata=metadata,
#             response_time=llm_response.get('response_time'),
#             token_count=llm_response.get('token_count')
#         )
        
#         # 更新会话时间
#         session.save()
        
#         # 返回响应
#         return Response({
#             'session_id': str(session.id),
#             'session_title': session.title,
#             'message_id': str(assistant_message.id),
#             'response': llm_response['response'],
#             'metadata': metadata,
#             'response_time': llm_response.get('response_time'),
#             'success': llm_response.get('success', True)
#         })
        
#     except Exception as e:
#         return Response(
#             {'error': f'聊天处理失败: {str(e)}'}, 
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )


# @api_view(['GET'])
# @permission_classes([IsAdminUser])
# def rag_system_stats_view(request):
#     """RAG系统统计信息视图"""
#     try:
#         # 文档统计
#         total_documents = KnowledgeDocument.objects.count()
#         indexed_documents = KnowledgeDocument.objects.filter(status='indexed').count()
#         processing_documents = KnowledgeDocument.objects.filter(status='processing').count()
#         failed_documents = KnowledgeDocument.objects.filter(status='failed').count()
        
#         # 会话统计
#         total_sessions = ChatSession.objects.count()
#         active_sessions = ChatSession.objects.filter(is_active=True).count()
#         total_messages = ChatMessage.objects.count()
        
#         # 向量数据库统计
#         vector_service = VectorService()
#         vector_stats = vector_service.get_collection_stats()
        
#         # LLM服务健康检查
#         llm_service = LLMService()
#         llm_health = llm_service.check_service_health()
        
#         return Response({
#             'documents': {
#                 'total': total_documents,
#                 'indexed': indexed_documents,
#                 'processing': processing_documents,
#                 'failed': failed_documents
#             },
#             'conversations': {
#                 'total_sessions': total_sessions,
#                 'active_sessions': active_sessions,
#                 'total_messages': total_messages
#             },
#             'vector_database': vector_stats,
#             'llm_service': llm_health,
#             'system_status': 'healthy' if llm_health.get('service_available') else 'degraded'
#         })
        
#     except Exception as e:
#         return Response(
#             {'error': f'获取统计信息失败: {str(e)}'}, 
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
# RAG and AI views @end

# ==== 新增：薪资计算/批量生成接口（与前端保持一致） ====
@api_view(['POST'])
@permission_classes([IsAdminUser])
def calculate_salary_by_employee_view(request, employee_id):
    """根据员工 UUID 计算并创建单条薪资记录（前端 /api/salaries/calculate/<employee_id>/）"""
    # 解析请求数据
    salary_period = request.data.get('salary_period')
    bonus = Decimal(str(request.data.get('bonus', 0)))
    deduction = Decimal(str(request.data.get('deduction', request.data.get('deductions', 0))))

    # 基本校验
    if not salary_period or not re.match(r'^\d{4}-\d{2}$', str(salary_period)):
        return Response({'success': False, 'error': '薪资期间格式应为 YYYY-MM'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return Response({'success': False, 'error': '员工不存在'}, status=status.HTTP_404_NOT_FOUND)

    # 检查重复
    if SalaryRecord.objects.filter(employee=employee, salary_period=salary_period).exists():
        return Response({'success': False, 'error': '该员工在此期间已有薪资记录'}, status=status.HTTP_400_BAD_REQUEST)

    # 计算薪资
    base_salary = employee.base_salary
    gross_salary = base_salary + bonus
    net_salary = gross_salary - deduction

    salary_record = SalaryRecord.objects.create(
        employee=employee,
        salary_period=salary_period,
        position_snapshot=employee.position,
        base_salary_snapshot=base_salary,
        bonus=bonus,
        deductions=deduction,
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
    """为所有员工批量生成薪资记录（前端 /api/salaries/generate/）"""
    salary_period = request.data.get('salary_period')
    bonus = Decimal(str(request.data.get('bonus', 0)))
    deduction = Decimal(str(request.data.get('deduction', request.data.get('deductions', 0))))

    # 校验
    if not salary_period or not re.match(r'^\d{4}-\d{2}$', str(salary_period)):
        return Response({'success': False, 'error': '薪资期间格式应为 YYYY-MM'}, status=status.HTTP_400_BAD_REQUEST)

    created_records = []
    skipped_employees = []

    for employee in Employee.objects.all():
        # 跳过已存在记录
        if SalaryRecord.objects.filter(employee=employee, salary_period=salary_period).exists():
            skipped_employees.append(employee.employee_id)
            continue

        base_salary = employee.base_salary
        gross_salary = base_salary + bonus
        net_salary = gross_salary - deduction

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

# ==== 结束新增 ====