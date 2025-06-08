#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Employee, Department

def update_employee_departments():
    """更新员工的部门关联"""
    
    # 获取所有部门
    departments = {dept.name: dept for dept in Department.objects.all()}
    print(f"Available departments: {list(departments.keys())}")
    
    # 获取所有员工
    employees = Employee.objects.all()
    print(f"Total employees: {employees.count()}")
    
    updated_count = 0
    for employee in employees:
        # 根据员工的部门名称找到对应的部门对象
        if employee.department in departments:
            dept_obj = departments[employee.department]
            if employee.department_ref != dept_obj:
                employee.department_ref = dept_obj
                employee.save()
                print(f"Updated {employee.name} -> {dept_obj.name}")
                updated_count += 1
        else:
            print(f"Warning: No department found for {employee.name} (department: {employee.department})")
    
    print(f"Updated {updated_count} employees")

if __name__ == '__main__':
    update_employee_departments() 