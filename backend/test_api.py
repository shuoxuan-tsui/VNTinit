#!/usr/bin/env python3
"""
API测试脚本
用于验证Django REST API端点是否正常工作
"""

import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

def test_api_endpoints():
    """测试API端点"""
    print("🚀 开始测试API端点...")
    
    # 测试登录端点
    print("\n1. 测试登录端点...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'  # 使用创建超级用户时设置的密码
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"   ✅ 登录成功，获取到Token: {token[:20]}...")
            
            # 使用Token测试其他端点
            headers = {'Authorization': f'Token {token}'}
            
            # 测试获取当前用户信息
            print("\n2. 测试获取当前用户信息...")
            response = requests.get(f'{BASE_URL}/auth/user/', headers=headers)
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                user_data = response.json()
                print(f"   ✅ 用户信息: {user_data['username']} (管理员: {user_data['is_superuser']})")
            
            # 测试员工列表端点
            print("\n3. 测试员工列表端点...")
            response = requests.get(f'{BASE_URL}/employees/', headers=headers)
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ 员工列表端点正常")
            
            # 测试薪资列表端点
            print("\n4. 测试薪资列表端点...")
            response = requests.get(f'{BASE_URL}/salaries/', headers=headers)
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ 薪资列表端点正常")
                
        else:
            print(f"   ❌ 登录失败: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ 无法连接到服务器，请确保Django服务器正在运行")
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")

if __name__ == '__main__':
    test_api_endpoints()
    print("\n🎉 API测试完成！") 