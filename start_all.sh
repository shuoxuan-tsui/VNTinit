#!/usr/bin/env fish

# 企业管理系统启动脚本
echo "🚀 启动企业管理系统..."

# 检查是否在正确的目录
if not test -d backend; or not test -d frontend
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
end

# 启动后端服务
echo "📡 启动Django后端服务..."
cd backend
if not test -d venv
    echo "❌ 错误：未找到虚拟环境，请先创建虚拟环境"
    exit 1
end

# 激活虚拟环境
source venv/bin/activate.fish

# 检查 Django 是否安装
if not python3 -c "import django" 2>/dev/null
    echo "❌ 错误：Django 未安装，正在安装..."
    pip install django
    if test $status -ne 0
        echo "❌ 错误：Django 安装失败，请检查 pip 和网络"
        exit 1
    end
end

# 启动 Django
python3 manage.py runserver 0.0.0.0:8000 &
set BACKEND_PID $last_pid
echo "✅ 后端服务已启动 (PID: $BACKEND_PID) - http://localhost:8000"

# 返回根目录
cd ..

# 启动前端服务
echo "🎨 启动Nuxt.js前端服务..."
cd frontend
npm run dev &
set FRONTEND_PID $last_pid
echo "✅ 前端服务已启动 (PID: $FRONTEND_PID) - http://localhost:3000"

# 返回根目录
cd ..

echo ""
echo "🎉 系统启动完成！"
echo "📱 前端地址: http://localhost:3000"
echo "🔧 后端API: http://localhost:8000"
echo "👤 默认管理员账户: admin / admin123"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 捕获 Ctrl+C 停止服务
function on_termination --on-signal SIGINT
    echo ''
    echo '🛑 正在停止服务...'
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo '✅ 所有服务已停止'
    exit 0
end

# 保持脚本运行
wait