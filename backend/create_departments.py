#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from api.models import Department

def create_departments():
    departments = [
        {
            'name': '技术部', 
            'code': 'TECH', 
            'description': '负责产品研发、技术架构设计和系统维护', 
            'manager': '李技术', 
            'manager_title': '技术总监',
            'location': '北京总部A座10-15层',
            'phone': '010-12345678-1001',
            'email': 'tech@example.com',
            'budget': 2500000
        },
        {
            'name': '人事部', 
            'code': 'HR', 
            'description': '负责人力资源管理、招聘和员工关系', 
            'manager': '张人事', 
            'manager_title': '人事经理',
            'location': '北京总部C座3层',
            'phone': '010-12345678-3001',
            'email': 'hr@example.com',
            'budget': 1200000
        },
        {
            'name': '财务部', 
            'code': 'FIN', 
            'description': '负责财务管理、预算控制和会计核算', 
            'manager': '赵财务', 
            'manager_title': '财务经理',
            'location': '北京总部C座2层',
            'phone': '010-12345678-4001',
            'email': 'finance@example.com',
            'budget': 1000000
        },
        {
            'name': '市场部', 
            'code': 'MKT', 
            'description': '负责市场推广、品牌建设和客户关系维护', 
            'manager': '王市场', 
            'manager_title': '市场总监',
            'location': '北京总部B座5-7层',
            'phone': '010-12345678-2001',
            'email': 'marketing@example.com',
            'budget': 1800000
        },
        {
            'name': '运营部', 
            'code': 'OPS', 
            'description': '负责业务运营、流程优化和数据分析', 
            'manager': '刘运营', 
            'manager_title': '运营经理',
            'location': '北京总部B座8-9层',
            'phone': '010-12345678-5001',
            'email': 'operations@example.com',
            'budget': 1500000
        }
    ]
    
    # for dept_data in departments:
    #     dept, created = Department.objects.get_or_create(
    #         name=dept_data['name'], 
    #         defaults=dept_data
    #     )
    #     if created:
    #         print(f'Created department: {dept.name}')
    #     else:
    #         print(f'Department already exists: {dept.name}')
    
    # print(f'Total departments: {Department.objects.count()}')

    for dept_date in departments:
        dept, created = Department.objects.get_or_create(
            name = dept_date['name'],
            defaults = dept_date
        )
        if created:
            print(f'Created department: {dept.name}')
        else:
            print(f"Department already exists: {dept.name}")

    print(f'Total departments: {Department.objects.count()}')

if __name__ == '__main__':
    create_departments() 