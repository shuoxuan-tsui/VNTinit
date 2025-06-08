from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department, Employee, SalaryRecord
from decimal import Decimal
import re
from datetime import datetime


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
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'name', 'gender', 'department', 'department_name',
            'position', 'phone', 'hire_date', 'birth_date', 
            'base_salary', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'department_name', 'created_at', 'updated_at']
    
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
    """薪资计算序列化器"""
    employee_id = serializers.CharField()
    salary_period = serializers.CharField()
    bonus = serializers.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    deductions = serializers.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    def validate_employee_id(self, value):
        """验证员工ID"""
        try:
            employee = Employee.objects.get(employee_id=value)
            return value
        except Employee.DoesNotExist:
            raise serializers.ValidationError("员工不存在")
    
    def validate_salary_period(self, value):
        """验证薪资期间格式"""
        if not re.match(r'^\d{4}-\d{2}$', value):
            raise serializers.ValidationError("薪资期间格式应为 YYYY-MM")
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


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    groups = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_superuser', 'groups']
        read_only_fields = ['id', 'is_superuser', 'groups'] 