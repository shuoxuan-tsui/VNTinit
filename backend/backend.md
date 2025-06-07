# Django + PostgreSQL 后端 API 设计文档

## 技术栈

- **Django 5.2.1** - Web 框架
- **Django REST Framework 3.16.0** - API 框架
- **PostgreSQL** - 数据库
- **Django CORS Headers 4.7.0** - 跨域支持
- **Token Authentication** - 认证机制

## 项目结构

```
backend/
├── core/                 # Django项目核心配置
│   ├── settings.py      # 项目设置
│   ├── urls.py          # 主URL配置
│   └── wsgi.py          # WSGI配置
├── api/                 # API应用
│   ├── models.py        # 数据模型
│   ├── serializers.py   # 序列化器
│   ├── views.py         # 视图
│   ├── urls.py          # API路由
│   ├── permissions.py   # 权限控制
│   ├── admin.py         # Django管理界面
│   └── migrations/      # 数据库迁移文件
├── venv/                # 虚拟环境
├── requirements.txt     # Python依赖
├── manage.py           # Django管理脚本
└── test_api.py         # API测试脚本
```

## 已完成的配置

### 1. Django 设置 (core/settings.py)

✅ **已配置项目**：

- REST Framework 配置
- CORS 跨域设置
- Token 认证
- PostgreSQL 数据库连接
- 中文本地化设置
- 日志配置
- 安全设置

### 2. 数据模型 (api/models.py)

✅ **Employee 模型**：

- UUID 主键
- 工号唯一性约束
- 完整的员工信息字段
- 数据验证和索引优化

✅ **SalaryRecord 模型**：

- 薪资记录管理
- 员工关联外键
- 自动薪资计算
- 唯一性约束（员工+期间）

### 3. API 序列化器 (api/serializers.py)

✅ **数据验证**：

- 员工信息验证（工号唯一性、手机号格式等）
- 薪资数据验证（期间格式、数值范围等）
- 交叉验证（年龄检查、重复记录检查）

### 4. 权限控制 (api/permissions.py)

✅ **权限类**：

- `IsAdminOrReadOnly`: 管理员可写，普通用户只读
- `IsAdminUser`: 仅管理员可访问
- `IsSalaryOwnerOrAdmin`: 薪资记录所有者或管理员可访问

### 5. API 视图 (api/views.py)

✅ **认证端点**：

- 登录/登出
- 获取当前用户信息

✅ **员工管理**：

- 列表查询（支持搜索、筛选、分页）
- 创建、更新、删除员工
- 员工详情查看

✅ **薪资管理**：

- 薪资记录列表（管理员）
- 薪资计算和创建
- 薪资记录详情、更新、删除
- 打印视图
- 员工薪资历史

### 6. URL 路由 (api/urls.py)

✅ **API 端点**：

```
/api/v1/auth/login/                    # 登录
/api/v1/auth/logout/                   # 登出
/api/v1/auth/user/                     # 当前用户信息
/api/v1/employees/                     # 员工列表/创建
/api/v1/employees/{id}/                # 员工详情/更新/删除
/api/v1/employees/{employee_id}/salary/ # 员工薪资历史
/api/v1/salaries/                      # 薪资记录列表
/api/v1/salaries/{id}/                 # 薪资记录详情/更新/删除
/api/v1/salaries/calculate_and_create/ # 计算并创建薪资
/api/v1/salaries/{record_id}/print_view/ # 薪资打印视图
```

### 7. Django 管理界面 (api/admin.py)

✅ **管理界面配置**：

- 员工管理界面（搜索、筛选、分组显示）
- 薪资记录管理界面
- 只读字段和权限控制

## 数据模型设计

### 1. Employee (员工模型)

```python
class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    employee_id = models.CharField(max_length=20, unique=True)  # 工号
    name = models.CharField(max_length=100)  # 姓名
    gender = models.CharField(max_length=10, choices=[('M', '男'), ('F', '女')])
    department = models.CharField(max_length=100)  # 部门
    position = models.CharField(max_length=100)  # 职称/职务
    phone = models.CharField(max_length=20, blank=True)  # 电话
    hire_date = models.DateField()  # 入职日期
    birth_date = models.DateField(blank=True, null=True)  # 出生日期
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)  # 基础工资
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 2. SalaryRecord (薪资记录模型)

```python
class SalaryRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary_period = models.CharField(max_length=7)  # 薪资期间 (YYYY-MM)
    position_snapshot = models.CharField(max_length=100)  # 职称快照
    base_salary_snapshot = models.DecimalField(max_digits=10, decimal_places=2)  # 基础工资快照
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 奖金
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 扣除
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)  # 应发工资
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)  # 实发工资
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 权限控制

### 用户角色

1. **普通用户**：

   - 查看员工列表（可能有范围限制）
   - 查看自己的薪资记录
   - 查看员工详情

2. **管理员** (`is_superuser=True` 或 `groups=['Admin']`)：
   - 所有普通用户权限
   - 创建、编辑、删除员工
   - 查看所有薪资记录
   - 计算并生成薪资记录
   - 编辑、删除薪资记录

### 权限实现

- 使用 Django REST Framework 的权限类
- 自定义权限类检查用户角色
- 在视图中应用权限装饰器

## 数据验证

### 员工数据验证

- 工号唯一性检查
- 电话号码格式验证
- 日期格式验证
- 必填字段检查

### 薪资数据验证

- 薪资期间格式验证
- 数值范围检查
- 员工存在性验证

## 业务逻辑

### 薪资计算逻辑

```python
def calculate_salary(employee, salary_period, bonus=0, deductions=0):
    # 基础工资 = 员工当前基础工资
    base_salary = employee.base_salary

    # 应发工资 = 基础工资 + 奖金
    gross_salary = base_salary + bonus

    # 实发工资 = 应发工资 - 扣除
    net_salary = gross_salary - deductions

    return {
        'base_salary_snapshot': base_salary,
        'bonus': bonus,
        'deductions': deductions,
        'gross_salary': gross_salary,
        'net_salary': net_salary
    }
```

## 数据库配置

### PostgreSQL 设置

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vntdb',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 安全考虑

1. **认证**：使用 Token 认证
2. **CORS**：配置允许的前端域名
3. **数据验证**：严格的输入验证
4. **权限检查**：每个 API 端点都有适当的权限检查
5. **SQL 注入防护**：使用 Django ORM
6. **XSS 防护**：输出转义

## 性能优化

1. **数据库索引**：在常用查询字段上添加索引
2. **分页**：大数据集使用分页
3. **查询优化**：使用 select_related 和 prefetch_related
4. **缓存**：对不经常变化的数据使用缓存

## 开发环境设置

### 1. 环境准备

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境 (Linux/Mac)
source venv/bin/activate
# 或者在fish shell中
source venv/bin/activate.fish

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库设置

```bash
# 创建迁移文件
python manage.py makemigrations

# 运行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 3. 启动开发服务器

```bash
# 启动Django开发服务器
python manage.py runserver 0.0.0.0:8000
```

### 4. 测试 API

```bash
# 运行API测试脚本
python test_api.py
```

## 部署配置

### 环境变量

- `DEBUG`: 调试模式
- `SECRET_KEY`: Django 密钥
- `DATABASE_URL`: 数据库连接字符串
- `ALLOWED_HOSTS`: 允许的主机名
- `CORS_ALLOWED_ORIGINS`: 允许的 CORS 源

### 生产环境设置

- 使用 Gunicorn 作为 WSGI 服务器
- 使用 Nginx 作为反向代理
- 配置 SSL 证书
- 设置日志记录
- 配置静态文件服务

## 下一步计划

1. **前后端集成**：连接 Nuxt.js 前端
2. **用户认证增强**：JWT 令牌、刷新令牌
3. **数据导入导出**：Excel 文件处理
4. **报表功能**：薪资统计报表
5. **单元测试**：API 端点测试覆盖
6. **性能监控**：API 响应时间监控
7. **文档生成**：Swagger/OpenAPI 文档
