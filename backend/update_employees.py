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
    
    """
    Department.objects.all() 返回一个QuerySet对象，
    它是一个惰性执行的查询集，不会立即执行查询。
    只有在需要时，才会执行查询。
    惰性执行的优点是： 可以避免不必要的查询，加载不必要的字段和关联对象，提高查询效率。
    数据库执行查询并返回结果集。Django ORM 会将这些原始的数据库行数据映射回 Python 对象，即 Department 模型实例，然后将这些实例填充到 QuerySet 中，供你的代码使用。
    """
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
            # update dept_obj to employee.department_ref
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