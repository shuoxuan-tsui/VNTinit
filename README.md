# 企业管理系统 (VNTinit)

一个现代化的企业管理系统，基于 Vue.js/Nuxt.js 前端和 Django REST API 后端构建。

## ✨ 功能特性

- 🔐 **用户认证系统** - 登录、注册、密码管理
- 👥 **员工管理** - 员工信息的增删改查
- 💰 **薪资管理** - 薪资计算、记录和查询
- 📊 **数据统计** - 员工和薪资数据的可视化
- 🎨 **现代化 UI** - 响应式设计，支持深色模式
- 🔒 **权限控制** - 基于角色的访问控制

## 🛠 技术栈

### 前端

- **Nuxt.js 3** - Vue.js 全栈框架
- **Vue.js 3** - 渐进式 JavaScript 框架
- **Tailwind CSS** - 实用优先的 CSS 框架
- **Pinia** - Vue 状态管理
- **Nuxt Icon** - 图标组件库

### 后端

- **Django 5.2.1** - Python Web 框架
- **Django REST Framework** - API 开发框架
- **PostgreSQL** - 关系型数据库
- **Token 认证** - 基于 Token 的身份验证

## 🚀 快速开始

### 方式一：一键启动（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd VNTinit

# 首次运行需要初始化后端
./start_backend.sh

# 一键启动前后端服务
./start_all.sh
```

### 方式二：分别启动

#### 后端启动

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动服务
python manage.py runserver 0.0.0.0:8000
```

#### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 🌐 访问地址

- **前端应用**: http://localhost:3000
- **后端 API**: http://localhost:8000
- **Django 管理后台**: http://localhost:8000/admin

## 👤 默认账户

- **用户名**: `admin`
- **密码**: `admin123`
- **邮箱**: `admin@example.com`

## 🗄️ 测试数据生成

为了方便测试和演示，项目提供了批量生成员工信息的脚本：

### 使用方法

```bash
# 进入后端目录
cd backend

# 方式一：使用包装器脚本（推荐）
./generate_employees.sh 50    # 生成50个员工
./generate_employees.sh       # 交互式运行

# 方式二：直接运行Python脚本
source venv/bin/activate
python3 test.py 100          # 生成100个员工
python3 test.py              # 交互式运行
```

### 生成的数据包括

- **员工基本信息**: 姓名、性别、出生日期、联系方式
- **工作信息**: 部门、职位、入职日期、基本工资
- **薪资记录**: 自动为每个员工生成最近3个月的薪资记录

### 数据特点

- 🎯 **真实性**: 使用中文姓名、合理的工资范围、符合逻辑的日期
- 🔄 **随机性**: 所有数据都是随机生成，避免重复
- 📊 **完整性**: 包含员工信息和对应的薪资记录
- 🛡️ **安全性**: 自动检查重复的员工编号，确保数据唯一性

### 支持的部门和职位

**部门**: 人力资源部、财务部、技术部、市场部、销售部、运营部、客服部、行政部、法务部、采购部、研发部、产品部、设计部、质量部、安全部

**职位**: 经理、主管、专员、助理、总监、工程师、分析师、顾问、协调员、代表、高级工程师、资深专员、项目经理、产品经理、技术总监

## 📱 界面预览

### 登录页面

- 🎨 **丰富背景**: 渐变色彩、动态几何图形、毛玻璃效果
- 🔒 **安全验证**: 表单验证、密码可见性切换
- 📱 **响应式设计**: 适配各种屏幕尺寸
- ✨ **动画效果**: 平滑过渡、悬停效果

### 主要特色

- 背景采用多层次装饰元素，包括：
  - 大型模糊圆形渐变
  - 中等大小的动态圆形
  - 小装饰点的闪烁效果
  - SVG 几何线条动画
- 毛玻璃效果的登录表单
- 平滑的动画过渡效果

## 🔧 API 接口

### 认证相关

- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/register/` - 用户注册
- `POST /api/auth/logout/` - 用户登出
- `GET /api/auth/user/` - 获取当前用户信息
- `POST /api/auth/change-password/` - 修改密码
- `GET /api/auth/check/` - 检查认证状态

### 员工管理

- `GET /api/employees/` - 获取员工列表
- `POST /api/employees/` - 创建员工
- `GET /api/employees/{id}/` - 获取员工详情
- `PUT /api/employees/{id}/` - 更新员工信息
- `DELETE /api/employees/{id}/` - 删除员工

### 薪资管理

- `GET /api/salaries/` - 获取薪资记录列表
- `POST /api/salaries/calculate_and_create/` - 计算并创建薪资记录
- `GET /api/salaries/{id}/` - 获取薪资记录详情
- `PUT /api/salaries/{id}/` - 更新薪资记录
- `DELETE /api/salaries/{id}/` - 删除薪资记录

## 📁 项目结构

```
VNTinit/
├── backend/                 # Django后端
│   ├── api/                # API应用
│   │   ├── models.py       # 数据模型
│   │   ├── views.py        # API视图
│   │   ├── serializers.py  # 序列化器
│   │   └── urls.py         # URL路由
│   ├── core/               # 核心配置
│   └── requirements.txt    # Python依赖
├── frontend/               # Nuxt.js前端
│   ├── pages/              # 页面组件
│   ├── components/         # 可复用组件
│   ├── composables/        # 组合式函数
│   ├── stores/             # Pinia状态管理
│   ├── middleware/         # 中间件
│   └── assets/             # 静态资源
├── start_backend.sh        # 后端启动脚本
├── start_frontend.sh       # 前端启动脚本
├── start_all.sh           # 一键启动脚本
└── README.md              # 项目说明
```

## 🔧 开发指南

### 环境要求

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### 开发模式

```bash
# 后端开发
cd backend
source venv/bin/activate
python manage.py runserver

# 前端开发
cd frontend
npm run dev
```

### 生产部署

```bash
# 前端构建
cd frontend
npm run build

# 后端配置
cd backend
# 设置环境变量
export DEBUG=False
export ALLOWED_HOSTS=your-domain.com
python manage.py collectstatic
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🆘 问题反馈

如果您遇到任何问题，请在 [Issues](../../issues) 页面提交问题报告。

---

