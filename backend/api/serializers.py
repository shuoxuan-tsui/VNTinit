from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department, Employee, SalaryRecord
# , KnowledgeDocument, ChatSession, ChatMessage
from decimal import Decimal
import re
import os
from datetime import datetime
from django.conf import settings


class DepartmentSerializer(serializers.ModelSerializer):
    """部门序列化器"""
    employee_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'description', 'manager', 'manager_title',
            'location', 'phone', 'email', 'budget', 'status', 'employee_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'employee_count', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """验证部门名称唯一性"""
        if self.instance:
            # 更新时排除当前实例
            if Department.objects.exclude(pk=self.instance.pk).filter(name=value).exists():
                raise serializers.ValidationError("该部门名称已存在")
        else:
            # 创建时检查唯一性
            if Department.objects.filter(name=value).exists():
                raise serializers.ValidationError("该部门名称已存在")
        return value
    
    def validate_code(self, value):
        """验证部门代码唯一性"""
        if self.instance:
            # 更新时排除当前实例
            if Department.objects.exclude(pk=self.instance.pk).filter(code=value).exists():
                raise serializers.ValidationError("该部门代码已存在")
        else:
            # 创建时检查唯一性
            if Department.objects.filter(code=value).exists():
                raise serializers.ValidationError("该部门代码已存在")
        return value
    
    def validate_phone(self, value):
        """验证电话号码格式"""
        if value and not re.match(r'^[\d\-\+\(\)\s]+$', value):
            raise serializers.ValidationError("请输入有效的电话号码")
        return value
    
    def validate_budget(self, value):
        """验证预算"""
        if value < 0:
            raise serializers.ValidationError("预算不能为负数")
        return value


class EmployeeSerializer(serializers.ModelSerializer):
    """员工序列化器"""
    department_name = serializers.CharField(source='department_ref.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'name', 'gender', 'department', 'department_ref', 'department_name',
            'position', 'phone', 'hire_date', 'birth_date', 
            'base_salary', 'status', 'location', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'department', 'department_name', 'created_at', 'updated_at']
    
    def validate_employee_id(self, value):
        """验证工号唯一性"""
        if self.instance:
            # 更新时排除当前实例
            if Employee.objects.exclude(pk=self.instance.pk).filter(employee_id=value).exists():
                raise serializers.ValidationError("该工号已存在")
        else:
            # 创建时检查唯一性
            if Employee.objects.filter(employee_id=value).exists():
                raise serializers.ValidationError("该工号已存在")
        return value
    
    def validate_phone(self, value):
        """验证手机号格式"""
        if value and not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("请输入有效的手机号码")
        return value
    
    def validate_base_salary(self, value):
        """验证基础工资"""
        if value <= 0:
            raise serializers.ValidationError("基础工资必须大于0")
        return value
    
    def validate_hire_date(self, value):
        """验证入职日期"""
        if value > datetime.now().date():
            raise serializers.ValidationError("入职日期不能是未来日期")
        return value
    
    def validate(self, attrs):
        """交叉验证"""
        if 'birth_date' in attrs and 'hire_date' in attrs:
            if attrs['birth_date'] and attrs['hire_date']:
                # 计算入职时年龄，不能小于16岁
                age_at_hire = (attrs['hire_date'] - attrs['birth_date']).days / 365.25
                if age_at_hire < 16:
                    raise serializers.ValidationError("入职时年龄不能小于16岁")
        return attrs


class SalaryRecordSerializer(serializers.ModelSerializer):
    """薪资记录序列化器"""
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    department = serializers.CharField(source='employee.department', read_only=True)
    
    class Meta:
        model = SalaryRecord
        fields = [
            'id', 'employee', 'employee_id', 'employee_name', 'department',
            'salary_period', 'position_snapshot', 'base_salary_snapshot',
            'bonus', 'deductions', 'gross_salary', 'net_salary',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'gross_salary', 'net_salary', 'created_at', 'updated_at']
    
    def validate_salary_period(self, value):
        """验证薪资期间格式"""
        if not re.match(r'^\d{4}-\d{2}$', value):
            raise serializers.ValidationError("薪资期间格式应为 YYYY-MM")
        
        try:
            year, month = value.split('-')
            year, month = int(year), int(month)
            if month < 1 or month > 12:
                raise ValueError
        except ValueError:
            raise serializers.ValidationError("无效的薪资期间")
        
        return value
    
    def validate_bonus(self, value):
        """验证奖金"""
        if value < 0:
            raise serializers.ValidationError("奖金不能为负数")
        return value
    
    def validate_deductions(self, value):
        """验证扣除"""
        if value < 0:
            raise serializers.ValidationError("扣除不能为负数")
        return value
    
    def validate(self, attrs):
        """交叉验证"""
        employee = attrs.get('employee')
        salary_period = attrs.get('salary_period')
        
        # 检查同一员工同一期间是否已有记录
        if self.instance:
            # 更新时排除当前实例
            existing = SalaryRecord.objects.exclude(pk=self.instance.pk).filter(
                employee=employee, salary_period=salary_period
            )
        else:
            # 创建时检查
            existing = SalaryRecord.objects.filter(
                employee=employee, salary_period=salary_period
            )
        
        if existing.exists():
            raise serializers.ValidationError("该员工在此期间已有薪资记录")
        
        return attrs


class SalaryCalculationSerializer(serializers.Serializer):
    """Serializer for salary calculation
    
    This serializer handles the validation of salary calculation data including:
    - Employee ID validation
    - Salary period format validation
    - Bonus and deductions validation
    """
    employee_id = serializers.CharField()
    salary_period = serializers.CharField()
    bonus = serializers.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    deductions = serializers.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    def validate_employee_id(self, value):
        """Validate employee ID exists in database
        
        Args:
            value: Employee ID string to validate
            
        Returns:
            The validated employee ID if exists
            
        Raises:
            serializers.ValidationError: If employee doesn't exist
        """
        try:
            employee = Employee.objects.get(employee_id=value)
            return value
        except Employee.DoesNotExist:
            raise serializers.ValidationError("员工不存在")
    
    def validate_salary_period(self, value):
        """Validate salary period format (YYYY-MM)
        
        Args:
            value: Salary period string to validate
            
        Returns:
            The validated salary period string
            
        Raises:
            serializers.ValidationError: If format is invalid
        """
        if not re.match(r'^\d{4}-\d{2}$', value):
            raise serializers.ValidationError("薪资期间格式应为 YYYY-MM")
        return value
    
    def validate_bonus(self, value):
        """Validate bonus is non-negative
        
        Args:
            value: Bonus amount to validate
            
        Returns:
            The validated bonus amount
            
        Raises:
            serializers.ValidationError: If bonus is negative
        """
        if value < 0:
            raise serializers.ValidationError("奖金不能为负数")
        return value
    
    def validate_deductions(self, value):
        """Validate deductions is non-negative
        
        Args:
            value: Deductions amount to validate
            
        Returns:
            The validated deductions amount
            
        Raises:
            serializers.ValidationError: If deductions is negative
        """
        if value < 0:
            raise serializers.ValidationError("扣除不能为负数")
        return value

class UserSerializer(serializers.ModelSerializer):
    """User serializer for handling user data
    
    This serializer handles the serialization/deserialization of User model data.
    It includes basic user information and group membership details.
    
    Fields:
        id: The unique identifier for the user (read-only)
        username: The user's login name
        email: The user's email address
        is_superuser: Boolean indicating admin status (read-only)
        groups: List of group names the user belongs to (read-only)

        This model = User, User is built-in user model in django with basic fragment such as: username, password, is_active, is staff, is superuser, etc.
        In frontend, we use this fragment to signed a user is active or not.
        despite raise a error.

        serializer.stringrelatedfield is a read-only field that represents its targets using their plain string representation.
    """
    groups = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_superuser', 'groups']
        read_only_fields = ['id', 'is_superuser', 'groups']  # These fields cannot be modified via API


# class KnowledgeDocumentSerializer(serializers.ModelSerializer):
#     """知识文档序列化器"""
#     department_name = serializers.CharField(source='department.name', read_only=True)
#     uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
#     tags_list = serializers.SerializerMethodField()
    
#     class Meta:
#         model = KnowledgeDocument
#         fields = [
#             'id', 'title', 'description', 'document_type', 'file_name', 'file_size',
#             'content', 'status', 'chunk_count', 'department', 'department_name',
#             'tags', 'tags_list', 'uploaded_by', 'uploaded_by_name',
#             'created_at', 'updated_at'
#         ]
#         read_only_fields = [
#             'id', 'file_size', 'content', 'status', 'chunk_count',
#             'department_name', 'uploaded_by_name', 'created_at', 'updated_at'
#         ]
    
#     def get_tags_list(self, obj):
#         """获取标签列表"""
#         if obj.tags:
#             return [tag.strip() for tag in obj.tags.split(',') if tag.strip()]
#         return []
    
#     def validate_title(self, value):
#         """验证标题"""
#         if len(value.strip()) < 2:
#             raise serializers.ValidationError("标题至少需要2个字符")
#         return value.strip()
    
#     def validate_tags(self, value):
#         """验证标签"""
#         if value:
#             tags = [tag.strip() for tag in value.split(',')]
#             if len(tags) > 10:
#                 raise serializers.ValidationError("标签数量不能超过10个")
#             for tag in tags:
#                 if len(tag) > 20:
#                     raise serializers.ValidationError("单个标签长度不能超过20个字符")
#         return value


# class DocumentUploadSerializer(serializers.Serializer):
#     """文档上传序列化器"""
#     file = serializers.FileField()
#     title = serializers.CharField(max_length=200)
#     description = serializers.CharField(required=False, allow_blank=True)
#     document_type = serializers.ChoiceField(choices=KnowledgeDocument.DOCUMENT_TYPES)
#     department = serializers.UUIDField(required=False, allow_null=True)
#     tags = serializers.CharField(required=False, allow_blank=True)
    
#     def validate_file(self, value):
#         """验证上传文件"""
#         # 文件大小检查
#         if value.size > settings.MAX_DOCUMENT_SIZE:
#             raise serializers.ValidationError(
#                 f"文件大小超过限制 ({settings.MAX_DOCUMENT_SIZE // (1024*1024)}MB)"
#             )
        
#         # 文件类型检查
#         file_ext = os.path.splitext(value.name)[1].lower()
#         if file_ext not in settings.ALLOWED_DOCUMENT_TYPES:
#             raise serializers.ValidationError(f"不支持的文件类型: {file_ext}")
        
#         return value


# class ChatSessionSerializer(serializers.ModelSerializer):
#     """聊天会话序列化器"""
#     message_count = serializers.ReadOnlyField()
#     last_message = serializers.SerializerMethodField()
    
#     class Meta:
#         model = ChatSession
#         fields = [
#             'id', 'title', 'is_active', 'message_count', 'last_message',
#             'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'message_count', 'created_at', 'updated_at']
    
#     def get_last_message(self, obj):
#         """获取最后一条消息"""
#         last_msg = obj.messages.last()
#         if last_msg:
#             return {
#                 'content': last_msg.content[:100] + '...' if len(last_msg.content) > 100 else last_msg.content,
#                 'role': last_msg.role,
#                 'created_at': last_msg.created_at
#             }
#         return None


# class ChatMessageSerializer(serializers.ModelSerializer):
#     """聊天消息序列化器"""
    
#     class Meta:
#         model = ChatMessage
#         fields = [
#             'id', 'role', 'content', 'metadata', 'response_time',
#             'token_count', 'created_at'
#         ]
#         read_only_fields = ['id', 'response_time', 'token_count', 'created_at']


# class ChatRequestSerializer(serializers.Serializer):
#     """聊天请求序列化器"""
#     message = serializers.CharField(max_length=2000)
#     session_id = serializers.UUIDField(required=False, allow_null=True)
#     model = serializers.CharField(default="gpt-3.5-turbo", required=False)
    
#     def validate_message(self, value):
#         """验证消息内容"""
#         if len(value.strip()) < 1:
#             raise serializers.ValidationError("消息内容不能为空")
#         return value.strip()


# class DocumentSearchSerializer(serializers.Serializer):
#     """文档搜索序列化器"""
#     query = serializers.CharField(max_length=500)
#     document_type = serializers.ChoiceField(
#         choices=KnowledgeDocument.DOCUMENT_TYPES,
#         required=False,
#         allow_null=True
#     )
#     department = serializers.UUIDField(required=False, allow_null=True)
#     top_k = serializers.IntegerField(default=5, min_value=1, max_value=20)
    
#     def validate_query(self, value):
#         """验证查询内容"""
#         if len(value.strip()) < 2:
#             raise serializers.ValidationError("查询内容至少需要2个字符")
#         return value.strip()