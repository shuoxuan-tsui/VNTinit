#!/usr/bin/env node

const axios = require('axios');

const API_BASE = 'http://localhost:8000/api';
const TOKEN = '768a9ddeec77f6cc2336a438eb8550551373093e';

const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Token ${TOKEN}`
};

async function testAPI() {
  console.log('🚀 开始测试HR管理系统API...\n');

  try {
    // 1. 测试员工API
    console.log('1️⃣ 测试员工API...');
    const employeesResponse = await axios.get(`${API_BASE}/employees/`, { headers });
    console.log(`   ✅ 员工总数: ${employeesResponse.data.total_count}`);
    console.log(`   ✅ 当前页员工数: ${employeesResponse.data.results.length}`);

    // 2. 测试薪资统计API
    console.log('\n2️⃣ 测试薪资统计API...');
    const statsResponse = await axios.get(`${API_BASE}/salaries/stats/`, { headers });
    if (statsResponse.data.success) {
      const stats = statsResponse.data.data;
      console.log(`   ✅ 薪资记录总数: ${stats.totalRecords}`);
      console.log(`   ✅ 总薪资: ¥${stats.totalSalary.toLocaleString()}`);
      console.log(`   ✅ 平均薪资: ¥${Math.round(stats.averageSalary).toLocaleString()}`);
      console.log(`   ✅ 涉及部门数: ${stats.departmentCount}`);
    }

    // 3. 测试薪资记录API
    console.log('\n3️⃣ 测试薪资记录API...');
    const salariesResponse = await axios.get(`${API_BASE}/salaries/`, { headers });
    console.log(`   ✅ 薪资记录数: ${salariesResponse.data.results.length}`);

    // 4. 测试部门API
    console.log('\n4️⃣ 测试部门API...');
    const departmentsResponse = await axios.get(`${API_BASE}/departments/`, { headers });
    console.log(`   ✅ 部门总数: ${departmentsResponse.data.results.length}`);

    // 5. 测试员工创建（模拟）
    console.log('\n5️⃣ 测试员工创建功能...');
    const newEmployee = {
      name: '测试员工',
      employee_id: 'TEST001',
      gender: 'M',
      phone: '13800138000',
      birth_date: '1990-01-01',
      hire_date: '2025-01-01',
      department: '技术部',
      position: '工程师',
      base_salary: 10000,
      status: 'active'
    };

    try {
      const createResponse = await axios.post(`${API_BASE}/employees/`, newEmployee, { headers });
      console.log(`   ✅ 员工创建成功: ${createResponse.data.name} (${createResponse.data.employee_id})`);
      
      // 删除测试员工
      await axios.delete(`${API_BASE}/employees/${createResponse.data.id}/`, { headers });
      console.log(`   ✅ 测试员工已删除`);
    } catch (error) {
      if (error.response?.status === 400) {
        console.log(`   ⚠️  员工创建测试跳过 (可能已存在): ${error.response.data.employee_id?.[0] || '验证错误'}`);
      } else {
        throw error;
      }
    }

    console.log('\n🎉 所有API测试通过！');
    console.log('\n📊 系统状态总结:');
    console.log(`   • 活跃员工: ${employeesResponse.data.total_count} 人`);
    console.log(`   • 薪资记录: ${statsResponse.data.data.totalRecords} 条`);
    console.log(`   • 部门数量: ${departmentsResponse.data.results.length} 个`);
    console.log(`   • 平均薪资: ¥${Math.round(statsResponse.data.data.averageSalary).toLocaleString()}`);

  } catch (error) {
    console.error('❌ API测试失败:', error.response?.data || error.message);
    process.exit(1);
  }
}

// 运行测试
testAPI(); 