#!/bin/bash

echo "=== 企业管理系统 API 调试脚本 ==="
echo ""

# 检查后端服务
echo "1. 检查后端服务状态..."
if curl -s http://localhost:8000/api/ > /dev/null; then
    echo "✅ 后端服务正常运行 (端口 8000)"
else
    echo "❌ 后端服务未运行或无法访问"
    echo "请运行: cd backend && bash -c 'source venv/bin/activate && python manage.py runserver 0.0.0.0:8000'"
    exit 1
fi

# 检查前端服务
echo ""
echo "2. 检查前端服务状态..."
if curl -s http://localhost:3000/ > /dev/null; then
    echo "✅ 前端服务正常运行 (端口 3000)"
else
    echo "❌ 前端服务未运行或无法访问"
    echo "请运行: cd frontend && npm run dev"
    exit 1
fi

# 检查前端代理
echo ""
echo "3. 检查前端代理..."
if curl -s http://localhost:3000/api/ > /dev/null; then
    echo "✅ 前端代理正常工作"
else
    echo "❌ 前端代理配置有问题"
    exit 1
fi

# 测试注册API
echo ""
echo "4. 测试注册API..."
RANDOM_ID=$(date +%s)
TEST_USER="testuser$RANDOM_ID"
TEST_EMAIL="test$RANDOM_ID@example.com"

REGISTER_RESPONSE=$(curl -s -X POST http://localhost:3000/api/auth/register/ \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$TEST_USER\",\"email\":\"$TEST_EMAIL\",\"password\":\"testpass123\"}")

if echo "$REGISTER_RESPONSE" | grep -q '"success":true'; then
    echo "✅ 注册API正常工作"
    echo "响应: $REGISTER_RESPONSE"
else
    echo "❌ 注册API有问题"
    echo "响应: $REGISTER_RESPONSE"
fi

# 测试登录API
echo ""
echo "5. 测试登录API..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:3000/api/auth/login/ \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$TEST_USER\",\"password\":\"testpass123\"}")

if echo "$LOGIN_RESPONSE" | grep -q '"success":true'; then
    echo "✅ 登录API正常工作"
    echo "响应: $LOGIN_RESPONSE"
else
    echo "❌ 登录API有问题"
    echo "响应: $LOGIN_RESPONSE"
fi

echo ""
echo "=== 调试完成 ==="
echo ""