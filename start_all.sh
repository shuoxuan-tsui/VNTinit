#!/bin/bash

echo "🚀 启动VNT企业管理系统..."

# 检查端口是否被占用
check_port() {
    local port=$1
    local service=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ $service 已在端口 $port 运行"
        return 0
    else
        echo "❌ $service 未在端口 $port 运行"
        return 1
    fi
}

# 启动后端Django服务
start_backend() {
    echo "📡 启动后端Django服务..."
    cd backend
    
    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        echo "创建Python虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    source venv/bin/activate 2>/dev/null || echo "虚拟环境激活失败，使用系统Python"
    
    # 安装依赖
    if [ -f "requirements.txt" ]; then
        echo "安装Python依赖..."
        pip install -r requirements.txt
    fi
    
    # 数据库迁移
    echo "执行数据库迁移..."
    python manage.py migrate
    
    # 启动服务
    echo "启动Django开发服务器..."
    python manage.py runserver 0.0.0.0:8000 &
    BACKEND_PID=$!
    
    # 等待服务启动
    sleep 5
    
    if check_port 8000 "Django后端"; then
        echo "✅ 后端服务启动成功 (PID: $BACKEND_PID)"
    else
        echo "❌ 后端服务启动失败"
        return 1
    fi
    
    cd ..
}

# 启动前端Nuxt服务
start_frontend() {
    echo "🎨 启动前端Nuxt服务..."
    cd frontend
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js 未安装，请先安装Node.js"
        return 1
    fi
    
    # 安装依赖
    if [ ! -d "node_modules" ]; then
        echo "安装Node.js依赖..."
        npm install
    fi
    
    # 启动服务
    echo "启动Nuxt开发服务器..."
    npm run dev &
    FRONTEND_PID=$!
    
    # 等待服务启动
    sleep 10
    
    if check_port 3000 "Nuxt前端"; then
        echo "✅ 前端服务启动成功 (PID: $FRONTEND_PID)"
    else
        echo "❌ 前端服务启动失败"
        return 1
    fi
    
    cd ..
}

# 检查数据库连接
check_database() {
    echo "🗄️ 检查数据库连接..."
    
    # 使用Python检查数据库
    cd backend
    python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from django.db import connection
try:
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM api_employee')
    count = cursor.fetchone()[0]
    print(f'✅ 数据库连接正常，员工数据: {count} 条')
except Exception as e:
    print(f'❌ 数据库连接失败: {e}')
    exit(1)
" 2>/dev/null || echo "❌ 数据库检查失败"
    cd ..
}

# 主函数
main() {
    echo "开始启动所有服务..."
    
    # 检查现有服务
    if check_port 8000 "Django后端" && check_port 3000 "Nuxt前端"; then
        echo "🎉 所有服务已在运行！"
        echo ""
        echo "📋 服务状态:"
        echo "   后端API: http://localhost:8000"
        echo "   前端界面: http://localhost:3000"
        echo "   调试页面: http://localhost:3000/debug"
        echo ""
        echo "💡 测试建议:"
        echo "1. 访问 http://localhost:3000/debug 测试API连接"
        echo "2. 使用 admin/admin123 登录"
        echo "3. 访问员工管理页面查看数据"
        return 0
    fi
    
    # 检查数据库
    check_database
    
    # 启动后端
    if ! check_port 8000 "Django后端"; then
        start_backend || exit 1
    fi
    
    # 启动前端
    if ! check_port 3000 "Nuxt前端"; then
        start_frontend || exit 1
    fi
    
    echo ""
    echo "🎉 所有服务启动完成！"
    echo ""
    echo "📋 服务信息:"
    echo "   后端API: http://localhost:8000"
    echo "   前端界面: http://localhost:3000"
    echo "   调试页面: http://localhost:3000/debug"
    echo ""
    echo "🔐 默认登录信息:"
    echo "   用户名: admin"
    echo "   密码: admin123"
    echo ""
    echo "💡 使用说明:"
    echo "1. 首先访问调试页面测试API连接"
    echo "2. 点击'测试登录'按钮进行认证"
    echo "3. 点击'测试员工API'验证数据获取"
    echo "4. 然后访问正常的员工管理页面"
    echo ""
    echo "🛑 停止服务: Ctrl+C 或运行 pkill -f 'manage.py runserver' && pkill -f 'nuxt'"
}

# 信号处理
cleanup() {
    echo ""
    echo "🛑 正在停止服务..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    pkill -f "manage.py runserver" 2>/dev/null
    pkill -f "nuxt" 2>/dev/null
    echo "✅ 服务已停止"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 运行主函数
main

# 保持脚本运行
echo "按 Ctrl+C 停止所有服务..."
wait