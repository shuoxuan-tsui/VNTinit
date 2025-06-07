#!/usr/bin/env python3
"""
批量生成员工信息的自动化脚本
用于向PostgreSQL数据库中的vntdb数据库批量插入员工数据
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta, time
from decimal import Decimal
import uuid

# 添加Django项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 初始化Django
django.setup()

from api.models import Employee, SalaryRecord, Department, AttendanceRecord
from django.contrib.auth.models import User

class DataGenerator:
    """数据生成器，包含部门和员工信息"""
    
    def __init__(self):
        # 中文姓氏
        self.surnames = [
            '王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴',
            '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗',
            '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧',
            '程', '曹', '袁', '邓', '许', '傅', '沈', '曾', '彭', '吕'
        ]
        
        # 中文名字
        self.given_names = [
            '伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军',
            '洋', '勇', '艳', '杰', '娟', '涛', '明', '超', '秀兰', '霞',
            '平', '刚', '桂英', '建华', '文', '华', '金凤', '素英', '建国', '德华',
            '秀珍', '建军', '春梅', '海燕', '雪梅', '玉兰', '文华', '月英', '玉英', '玉华',
            '志强', '志明', '秀云', '桂花', '桂兰', '春花', '凤英', '玉梅', '海英', '丽娟'
        ]
        
        # 部门名称列表
        self.department_names = [
            '技术部', '市场部', '人力资源部', '财务部', '运营部', '客服部'
        ]
        
        # 职位列表
        self.positions = [
            '经理', '主管', '专员', '助理', '总监',
            '工程师', '分析师', '顾问', '协调员', '代表',
            '高级工程师', '资深专员', '项目经理', '产品经理', '技术总监'
        ]

        self.employee_statuses = ['active', 'on_leave', 'terminated']
        self.locations = ['北京总部', '上海分部', '广州研发中心', '深圳办公室', '远程办公']


    def generate_phone(self):
        """生成手机号码"""
        prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                   '150', '151', '152', '153', '155', '156', '157', '158', '159',
                   '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
        prefix = random.choice(prefixes)
        suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return prefix + suffix

    def generate_employee_id(self):
        """生成员工编号"""
        return f"EMP{datetime.now().year}{random.randint(10000, 99999)}"

    def generate_birth_date(self):
        """生成出生日期（22-60岁之间）"""
        current_year = datetime.now().year
        birth_year = random.randint(current_year - 60, current_year - 22)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # 避免月份天数问题
        return datetime(birth_year, birth_month, birth_day).date()

    def generate_hire_date(self, birth_date):
        """生成入职日期"""
        min_hire_year = birth_date.year + 18
        current_year = datetime.now().year
        
        if min_hire_year > current_year:
            min_hire_year = current_year
            
        hire_year = random.randint(min_hire_year, current_year)
        hire_month = random.randint(1, 12)
        hire_day = random.randint(1, 28)
        
        hire_date = datetime(hire_year, hire_month, hire_day).date()
        if hire_date > datetime.now().date():
            hire_date = datetime.now().date()
            
        return hire_date

    def generate_salary(self, department_name, position):
        """根据部门和职位生成基本工资"""
        base_salaries = {
            '技术部': {'经理': 25000, '主管': 18000, '工程师': 12000, '高级工程师': 15000, '专员': 8000, '总监': 30000},
            '市场部': {'经理': 22000, '主管': 16000, '专员': 9000, '助理': 6000, '总监': 29000},
            '人力资源部': {'经理': 20000, '主管': 14000, '专员': 8000, '助理': 5500, '总监': 27000},
            '财务部': {'经理': 24000, '主管': 17000, '专员': 10000, '助理': 6500, '总监': 30000},
            '运营部': {'经理': 21000, '主管': 15500, '专员': 8500, '助理': 6200, '总监': 27500},
            '客服部': {'经理': 19000, '主管': 13000, '专员': 7500, '协调员': 7000},
        }
        
        default_range = {'经理': 20000, '主管': 15000, '专员': 8000, '助理': 6000, '工程师': 12000, 
                         '总监': 28000, '高级工程师': 15000, '分析师': 10000, '顾问': 13000, 
                         '协调员': 7500, '代表': 7000, '项目经理': 18000, '产品经理': 20000}
        
        if department_name in base_salaries and position in base_salaries[department_name]:
            base = base_salaries[department_name][position]
        elif position in default_range:
            base = default_range[position]
        else:
            base = 8000 # Default for unmatched positions
            
        variation = random.uniform(0.8, 1.2)
        return Decimal(str(int(base * variation)))

    def generate_department_code(self, name):
        """Generates a simple department code based on name (e.g., HR for 人力资源部)"""
        code_map = {
            '技术部': 'TECH', '市场部': 'MKT', '人力资源部': 'HR', 
            '财务部': 'FIN', '运营部': 'OPS', '客服部': 'CS'
        }
        return code_map.get(name, name[:3].upper())


    def create_departments(self):
        """创建部门记录"""
        print("\n--- 正在创建部门 ---")
        created_count = 0
        for dept_name in self.department_names:
            if not Department.objects.filter(name=dept_name).exists():
                try:
                    surname = random.choice(self.surnames)
                    given_name = random.choice(self.given_names)
                    manager_name = surname + given_name
                    
                    Department.objects.create(
                        name=dept_name,
                        code=self.generate_department_code(dept_name),
                        description=f"{dept_name}的职责描述。",
                        manager=manager_name,
                        manager_title=f"{random.choice(['总监', '经理', '主管'])}",
                        location=random.choice(self.locations),
                        phone=self.generate_phone(),
                        email=f"{self.generate_department_code(dept_name).lower()}@example.com",
                        budget=Decimal(random.randint(500000, 5000000)),
                        status=random.choice(['active', 'inactive'])
                    )
                    print(f"✅ 已创建部门: {dept_name}")
                    created_count += 1
                except Exception as e:
                    print(f"❌ 创建部门 {dept_name} 失败: {e}")
            else:
                print(f"ℹ️  部门 {dept_name} 已存在，跳过创建。")
        print(f"部门创建完成，新增 {created_count} 个部门。")
        return Department.objects.all()


    def generate_employee_data(self, department_obj):
        """生成单个员工信息字典，关联到实际的Department对象"""
        surname = random.choice(self.surnames)
        given_name = random.choice(self.given_names)
        name = surname + given_name
        
        gender = random.choice(['M', 'F'])
        birth_date = self.generate_birth_date()
        hire_date = self.generate_hire_date(birth_date)
        
        position = random.choice(self.positions)
        phone = self.generate_phone()
        base_salary = self.generate_salary(department_obj.name, position)
        status = random.choice(self.employee_statuses)
        location = random.choice(self.locations) # Employee specific location
        notes = f"这是员工 {name} 的备注信息，{random.choice(['表现良好', '需要关注', '潜力巨大', ''])}" if random.choice([True, False]) else ""

        return {
            'employee_id': self.generate_employee_id(),
            'name': name,
            'gender': gender,
            'birth_date': birth_date,
            'phone': phone,
            'hire_date': hire_date,
            'department_ref': department_obj, # Link to Department object
            'position': position,
            'base_salary': base_salary,
            'status': status,
            'location': location,
            'notes': notes,
        }

    def create_employees(self, count=65): # Default to 65 employees
        """批量创建员工"""
        print("\n--- 正在创建员工 ---")
        
        departments = list(Department.objects.all())
        if not departments:
            print("⚠️  没有找到部门信息，请先创建部门。正在尝试自动创建...")
            self.create_departments()
            departments = list(Department.objects.all())
            if not departments:
                print("❌ 自动创建部门失败，无法继续创建员工。请检查 Department 模型和 create_departments 方法。")
                return

        created_count = 0
        failed_count = 0
        
        for i in range(count):
            try:
                # Randomly assign to an existing department
                department_obj = random.choice(departments)
                employee_data = self.generate_employee_data(department_obj)
                
                while Employee.objects.filter(employee_id=employee_data['employee_id']).exists():
                    employee_data['employee_id'] = self.generate_employee_id() # Regenerate if ID collision
                
                employee = Employee.objects.create(**employee_data)
                self.create_salary_records_for_employee(employee) # Create salary records for the new employee
                
                created_count += 1
                print(f"✅ 已创建员工 {i+1}/{count}: {employee.name} ({employee.employee_id}) in {department_obj.name}")
                
            except Exception as e:
                failed_count += 1
                print(f"❌ 创建员工 {i+1} 失败: {str(e)}")
                import traceback
                traceback.print_exc()

        print(f"\n🎉 员工批量创建完成!")
        print(f"✅ 成功创建: {created_count} 个员工")
        print(f"❌ 创建失败: {failed_count} 个员工")

    def create_salary_records_for_employee(self, employee):
        """为单个员工创建最近3个月的薪资记录"""
        current_date = datetime.now().date()
        
        for i in range(3): # Last 3 months
            month_offset = i
            target_date = current_date - timedelta(days=month_offset * 30) # Approximate month
            year = target_date.year
            month = target_date.month
            
            salary_period = f"{year:04d}-{month:02d}"
            
            if SalaryRecord.objects.filter(employee=employee, salary_period=salary_period).exists():
                # print(f"ℹ️  薪资记录已存在: {employee.name} - {salary_period}")
                continue
            
            base_salary = employee.base_salary
            bonus = Decimal(str(random.randint(0, int(base_salary * Decimal('0.3'))))) # Bonus up to 30% of base
            deductions = Decimal(str(random.randint(int(base_salary * Decimal('0.05')), int(base_salary * Decimal('0.2'))))) 
            
            try:
                SalaryRecord.objects.create(
                    employee=employee,
                    salary_period=salary_period,
                    position_snapshot=employee.position,
                    base_salary_snapshot=base_salary,
                    bonus=bonus,
                    deductions=deductions,
                    # gross_salary and net_salary will be calculated by model's save() method
                )
                # print(f"💰 已为 {employee.name} 创建薪资记录: {salary_period}")
            except Exception as e:
                print(f"⚠️  为员工 {employee.name} 创建薪资记录 ({salary_period}) 失败: {str(e)}")

    def create_attendance_records_for_employee(self, employee):
        """为单个员工创建最近30天的考勤记录"""
        
        current_date = datetime.now().date()
        
        # 考勤状态权重（模拟真实情况）
        attendance_statuses = [
            ('present', 70),      # 正常出勤 70%
            ('late', 15),         # 迟到 15%
            ('early_leave', 5),   # 早退 5%
            ('sick_leave', 3),    # 病假 3%
            ('personal_leave', 2), # 事假 2%
            ('annual_leave', 3),  # 年假 3%
            ('absent', 2),        # 缺勤 2%
        ]
        
        # 创建权重列表
        weighted_statuses = []
        for status, weight in attendance_statuses:
            weighted_statuses.extend([status] * weight)
        
        for i in range(30):  # 最近30天
            attendance_date = current_date - timedelta(days=i)
            
            # 跳过周末（假设周六日不上班）
            if attendance_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                continue
            
            # 检查是否已存在记录
            if AttendanceRecord.objects.filter(employee=employee, date=attendance_date).exists():
                continue
            
            # 随机选择考勤状态
            status = random.choice(weighted_statuses)
            
            # 根据状态生成相应的时间和工时
            check_in_time = None
            check_out_time = None
            work_hours = Decimal('0.00')
            overtime_hours = Decimal('0.00')
            notes = ""
            
            if status in ['present', 'late', 'early_leave', 'overtime']:
                # 正常工作日的时间安排
                base_check_in = time(9, 0)  # 9:00 AM
                base_check_out = time(18, 0)  # 6:00 PM
                
                if status == 'present':
                    # 正常出勤：8:30-9:30之间签到，17:30-18:30之间签退
                    check_in_minutes = random.randint(8*60+30, 9*60+30)  # 8:30-9:30
                    check_out_minutes = random.randint(17*60+30, 18*60+30)  # 17:30-18:30
                    
                elif status == 'late':
                    # 迟到：9:30-10:30之间签到
                    check_in_minutes = random.randint(9*60+30, 10*60+30)
                    check_out_minutes = random.randint(17*60+30, 18*60+30)
                    notes = f"迟到 {random.randint(30, 90)} 分钟"
                    
                elif status == 'early_leave':
                    # 早退：正常签到，16:00-17:00之间签退
                    check_in_minutes = random.randint(8*60+30, 9*60+30)
                    check_out_minutes = random.randint(16*60, 17*60)
                    notes = f"早退 {random.randint(60, 120)} 分钟"
                    
                elif status == 'overtime':
                    # 加班：正常签到，19:00-22:00之间签退
                    check_in_minutes = random.randint(8*60+30, 9*60+30)
                    check_out_minutes = random.randint(19*60, 22*60)
                    overtime_hours = Decimal(str(random.uniform(1.0, 4.0)))
                    notes = f"加班 {float(overtime_hours):.1f} 小时"
                
                # 转换为时间对象
                check_in_time = time(check_in_minutes // 60, check_in_minutes % 60)
                check_out_time = time(check_out_minutes // 60, check_out_minutes % 60)
                
                # 计算工作时长
                check_in_total_minutes = check_in_minutes
                check_out_total_minutes = check_out_minutes
                
                # 减去午休时间（12:00-13:00）
                lunch_break = 60
                total_minutes = check_out_total_minutes - check_in_total_minutes - lunch_break
                work_hours = Decimal(str(max(0, total_minutes / 60.0)))
                
            elif status in ['sick_leave', 'personal_leave', 'annual_leave']:
                # 请假类型
                leave_reasons = {
                    'sick_leave': ['感冒发烧', '身体不适', '医院检查', '家人生病'],
                    'personal_leave': ['家庭事务', '个人事务', '搬家', '办理证件'],
                    'annual_leave': ['年假休息', '旅游度假', '回家探亲', '个人休假']
                }
                notes = random.choice(leave_reasons[status])
                
            elif status == 'absent':
                notes = "无故缺勤"
            
            try:
                AttendanceRecord.objects.create(
                    employee=employee,
                    date=attendance_date,
                    check_in_time=check_in_time,
                    check_out_time=check_out_time,
                    status=status,
                    work_hours=work_hours,
                    overtime_hours=overtime_hours,
                    notes=notes
                )
                
            except Exception as e:
                print(f"⚠️  为员工 {employee.name} 创建考勤记录 ({attendance_date}) 失败: {str(e)}")

    def create_all_attendance_records(self):
        """为所有员工创建考勤记录"""
        print("\n--- 正在创建考勤记录 ---")
        
        employees = Employee.objects.filter(status='active')
        total_employees = employees.count()
        
        if total_employees == 0:
            print("⚠️  没有找到活跃员工，跳过考勤记录创建。")
            return
        
        created_count = 0
        for index, employee in enumerate(employees, 1):
            try:
                self.create_attendance_records_for_employee(employee)
                created_count += 1
                print(f"✅ 已为员工 {employee.name} 创建考勤记录 ({index}/{total_employees})")
            except Exception as e:
                print(f"❌ 为员工 {employee.name} 创建考勤记录失败: {str(e)}")
        
        print(f"考勤记录创建完成，为 {created_count} 个员工创建了记录。")

    def create_all_data(self, num_employees=65):
        """统一入口，创建所有类型的数据"""
        print("🚀 开始生成所有数据...")
        self.create_departments()
        self.create_employees(num_employees)
        self.create_all_attendance_records()
        print("✅ 所有数据生成完毕 (部门、员工、薪资和考勤)。")


def main():
    """主函数"""
    print("=" * 60)
    print("🏢 企业管理系统 - 数据批量生成工具")
    print("=" * 60)
    
    try:
        from django.db import connection
        with connection.cursor() as cursor: # Ensure cursor is closed
            cursor.execute("SELECT 1")
        print("✅ 数据库连接成功")
        
        num_employees_to_generate = 65 # Default as per user request

        if len(sys.argv) > 1:
            try:
                count_arg = int(sys.argv[1])
                if 0 < count_arg <= 1000:
                    num_employees_to_generate = count_arg
                elif count_arg <= 0 :
                     print(f"⚠️  员工数量参数 ({count_arg}) 无效，将使用默认值 {num_employees_to_generate}。")
                else: # count_arg > 1000
                    print(f"⚠️  请求员工数量 ({count_arg}) 过大，将生成默认数量 {num_employees_to_generate} 以优化性能。")
                print(f"📝 将生成 {num_employees_to_generate} 个员工及其相关数据。")
            except ValueError:
                print(f"❌ 无效的员工数量参数。将使用默认值 {num_employees_to_generate}。")
        else:
            print(f"📝 将生成默认数量 {num_employees_to_generate} 个员工及其相关数据。")
            # confirm = input(f"\n确认要生成 {num_employees_to_generate} 个员工及其相关数据吗? (y/N): ").strip().lower()
            # if confirm not in ['y', 'yes']:
            #     print("❌ 操作已取消")
            #     return
        
        generator = DataGenerator()
        # 清空现有数据，确保从一个干净的状态开始（可选，但推荐用于测试）
        print("\n🧹 正在清理旧数据...")
        AttendanceRecord.objects.all().delete()
        SalaryRecord.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()
        print("🗑️ 旧数据清理完毕。")

        generator.create_all_data(num_employees_to_generate)
        
        total_departments = Department.objects.count()
        total_employees = Employee.objects.count()
        total_salary_records = SalaryRecord.objects.count()
        total_attendance_records = AttendanceRecord.objects.count()
        
        print(f"\n📈 数据库统计:")
        print(f"🏢 部门总数: {total_departments}")
        print(f"👥 员工总数: {total_employees}")
        print(f"💰 薪资记录总数: {total_salary_records}")
        print(f"📅 考勤记录总数: {total_attendance_records}")
        
    except Exception as e:
        print(f"❌ 程序执行出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 