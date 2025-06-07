#!/bin/bash

# 员工信息批量生成脚本包装器
# 使用方法: ./generate_employees.sh [员工数量]

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 检查虚拟环境
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "❌ 错误：未找到虚拟环境，请先运行 ./start_backend.sh"
    exit 1
fi

# 激活虚拟环境并运行Python脚本
cd "$SCRIPT_DIR"
source venv/bin/activate

if [ $# -eq 0 ]; then
    # 没有参数，交互式运行
    python3 test.py
else
    # 有参数，直接运行
    python3 test.py "$1"
fi 