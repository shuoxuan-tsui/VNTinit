from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from decimal import Decimal

# Create your models here.

class Department(models.Model):
    """部门模型"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='部门名称')
    code = models.CharField(max_length=20, unique=True, verbose_name='部门代码')
    description = models.TextField(blank=True, verbose_name='部门描述')
    manager = models.CharField(max_length=100, blank=True, verbose_name='部门经理')
    manager_title = models.CharField(max_length=100, blank=True, verbose_name='经理职位')
    location = models.CharField(max_length=200, blank=True, verbose_name='办公地点')
    phone = models.CharField(max_length=20, blank=True, verbose_name='部门电话')
    email = models.EmailField(blank=True, verbose_name='部门邮箱')
    budget = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00'),
        verbose_name='部门预算'
    )
    # choices 属性接受一个二元组，分别是value:字符
    status = models.CharField(
        max_length=20,
        choices=[('active', '活跃'), ('inactive', '停用')],
        default='active',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def employee_count(self):
        """获取部门员工数量"""
        return self.employees.count()
    
    def to_dict(self):
        """转换为字典格式，用于API响应"""
        return {
            'id': str(self.id),
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'manager': self.manager,
            'manager_title': self.manager_title,
            'location': self.location,
            'phone': self.phone,
            'email': self.email,
            'budget': float(self.budget),
            'status': self.status,
            'employee_count': self.employee_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class Employee(models.Model):
    """员工模型"""
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name='工号',
        help_text='员工唯一标识号'
    )
    name = models.CharField(max_length=100, verbose_name='姓名')
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        verbose_name='性别'
    )
    # 保持原来的字符串字段
    department = models.CharField(max_length=100, verbose_name='部门')
    # 新增外键字段，允许为空
    department_ref = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='employees',
        verbose_name='部门引用',
        null=True,
        blank=True
    )
    position = models.CharField(max_length=100, verbose_name='职称/职务')
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name='电话',
        validators=[
            RegexValidator(
                regex=r'^1[3-9]\d{9}$',
                message='请输入有效的手机号码'
            )
        ]
    )
    hire_date = models.DateField(verbose_name='入职日期')
    birth_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name='出生日期'
    )
    base_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='基础工资'
    )
    status = models.CharField(
        max_length=20, 
        choices=[('active', '在职'), ('on_leave', '休假'), ('terminated', '离职')], 
        default='active', 
        verbose_name='员工状态'
    )
    location = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name='员工办公地点'
    )
    notes = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='备注'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '员工'
        verbose_name_plural = '员工'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['department']),
            models.Index(fields=['position']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.employee_id} - {self.name}"
    
    def save(self, *args, **kwargs):
        # 同步部门名称
        if self.department_ref:
            self.department = self.department_ref.name
        super().save(*args, **kwargs)
    
    def to_dict(self):
        """转换为字典格式，用于API响应"""
        return {
            'id': str(self.id),
            'employee_id': self.employee_id,
            'name': self.name,
            'gender': self.gender,
            'department': self.department,
            'department_id': str(self.department_ref.id) if self.department_ref else None,
            'position': self.position,
            'phone': self.phone,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'base_salary': float(self.base_salary),
            'status': self.status,
            'location': self.location,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class SalaryRecord(models.Model):
    """薪资记录模型"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='salary_records',
        verbose_name='员工'
    )
    salary_period = models.CharField(
        max_length=7, 
        verbose_name='薪资期间',
        help_text='格式：YYYY-MM'
    )
    position_snapshot = models.CharField(
        max_length=100, 
        verbose_name='职称快照',
        help_text='记录计算薪资时的职称'
    )
    base_salary_snapshot = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='基础工资快照'
    )
    bonus = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        verbose_name='奖金'
    )
    deductions = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        verbose_name='扣除'
    )
    gross_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='应发工资'
    )
    net_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='实发工资'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '薪资记录'
        verbose_name_plural = '薪资记录'
        ordering = ['-created_at']
        unique_together = ['employee', 'salary_period']
        indexes = [
            models.Index(fields=['employee', 'salary_period']),
            models.Index(fields=['salary_period']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.employee.name} - {self.salary_period}"
    
    def to_dict(self):
        """转换为字典格式，用于API响应"""
        return {
            'id': str(self.id),
            'employee_id': self.employee.employee_id,
            'employee_name': self.employee.name,
            'department': self.employee.department,
            'position': self.position_snapshot,
            'salary_period': self.salary_period,
            'base_salary_snapshot': float(self.base_salary_snapshot),
            'bonus': float(self.bonus),
            'deductions': float(self.deductions),
            'gross_salary': float(self.gross_salary),
            'net_salary': float(self.net_salary),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
    
    def save(self, *args, **kwargs):
        """保存时自动计算薪资"""
        if not self.gross_salary:
            self.gross_salary = self.base_salary_snapshot + self.bonus
        if not self.net_salary:
            self.net_salary = self.gross_salary - self.deductions
        super().save(*args, **kwargs)


class AttendanceRecord(models.Model):
    """考勤记录模型"""
    ATTENDANCE_STATUS_CHOICES = [
        ('present', '出勤'),
        ('absent', '缺勤'),
        ('late', '迟到'),
        ('early_leave', '早退'),
        ('sick_leave', '病假'),
        ('personal_leave', '事假'),
        ('annual_leave', '年假'),
        ('overtime', '加班'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name='员工'
    )
    date = models.DateField(verbose_name='考勤日期')
    check_in_time = models.TimeField(
        blank=True, 
        null=True, 
        verbose_name='签到时间'
    )
    check_out_time = models.TimeField(
        blank=True, 
        null=True, 
        verbose_name='签退时间'
    )
    status = models.CharField(
        max_length=20,
        choices=ATTENDANCE_STATUS_CHOICES,
        default='present',
        verbose_name='考勤状态'
    )
    work_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='工作时长(小时)'
    )
    overtime_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='加班时长(小时)'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='备注'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '考勤记录'
        verbose_name_plural = '考勤记录'
        ordering = ['-date', '-created_at']
        unique_together = ['employee', 'date']
        indexes = [
            models.Index(fields=['employee', 'date']),
            models.Index(fields=['date']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.get_status_display()}"
    
    def to_dict(self):
        """转换为字典格式，用于API响应"""
        return {
            'id': str(self.id),
            'employee_id': self.employee.employee_id,
            'employee_name': self.employee.name,
            'department': self.employee.department,
            'date': self.date.isoformat(),
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'check_out_time': self.check_out_time.isoformat() if self.check_out_time else None,
            'status': self.status,
            'status_display': self.get_status_display(),
            'work_hours': float(self.work_hours),
            'overtime_hours': float(self.overtime_hours),
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
