from django.contrib import admin
from .models import Employee, SalaryRecord



# 注册Employee模型到Django Admin后台
# 这个类是继承自admin.ModelAdmin的子类，用于配置Employee模型的管理后台显示和行为
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # 定义在管理后台中显示的字段
    list_display = ['employee_id', 'name', 'gender', 'department', 'position', 'base_salary', 'hire_date', 'created_at']
    # 可过滤的字段
    list_filter = ['gender', 'department', 'position', 'hire_date']
    # 可搜索的字段
    search_fields = ['employee_id', 'name', 'department', 'position']
    # 可排序的字段
    ordering = ['-created_at']
    # 可只读的字段
    readonly_fields = ['id', 'created_at', 'updated_at']

    # 可编辑的字段
    fieldsets = (
        ('基本信息', {
            'fields': ('employee_id', 'name', 'gender', 'phone')
        }),
        ('工作信息', {
            'fields': ('department', 'position', 'base_salary', 'hire_date')
        }),
        ('个人信息', {
            'fields': ('birth_date',)
        }),
        ('系统信息', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# 注册SalaryRecord 模型到Django Admin后台
@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    # 定义在管理后台中显示的字段
    list_display = ['employee', 'salary_period', 'position_snapshot', 'base_salary_snapshot', 'bonus', 'deductions', 'net_salary', 'created_at']
    # 定义在管理后台中可以过滤的字段
    list_filter = ['salary_period', 'position_snapshot', 'created_at']
    # 定义在管理后台中可以搜索的字段
    search_fields = ['employee__name', 'employee__employee_id', 'salary_period']
    # 定义在管理后台中可以排序的字段
    ordering = ['-created_at']
    # 定义在管理后台中可以编辑的字段
    readonly_fields = ['id', 'gross_salary', 'net_salary', 'created_at', 'updated_at']
    
    # 定义在管理后台中可以编辑的字段
    fieldsets = (
        ('员工信息', {
            'fields': ('employee', 'salary_period', 'position_snapshot')
        }),
        ('薪资信息', {
            'fields': ('base_salary_snapshot', 'bonus', 'deductions', 'gross_salary', 'net_salary')
        }),
        ('系统信息', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    
    """
    定义在管理后台中可以编辑的字段
    这个方法用于设置哪些字段在编辑时是只读的
    params: request 请求对象, obj 要编辑的对象              
    return: 返回一个包含只读字段的列表
    """
    def get_readonly_fields(self, request, obj=None):
        if obj:  # 编辑现有对象
            return self.readonly_fields + ['employee', 'salary_period']
        return self.readonly_fields
