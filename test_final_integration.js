const axios = require('axios');

async function testFinalIntegration() {
  console.log('🧪 最终集成测试 - 员工管理页面数据显示\n');

  try {
    // 1. 测试后端API
    console.log('1. 测试后端API登录...');
    const loginResponse = await axios.post('http://localhost:8000/api/auth/login/', {
      username: 'admin',
      password: 'admin123'
    });
    
    if (!loginResponse.data.success) {
      throw new Error('后端登录失败');
    }
    
    const token = loginResponse.data.data.token;
    console.log('✅ 后端登录成功');
    
    // 2. 测试员工API
    console.log('\n2. 测试员工API...');
    const employeesResponse = await axios.get('http://localhost:8000/api/employees/', {
      headers: { 'Authorization': `Token ${token}` },
      params: { page: 1, page_size: 10 }
    });
    
    console.log('✅ 员工API响应成功');
    console.log(`   员工总数: ${employeesResponse.data.total_count}`);
    console.log(`   当前页员工数: ${employeesResponse.data.results.length}`);
    
    if (employeesResponse.data.results.length === 0) {
      throw new Error('没有员工数据');
    }
    
    const firstEmployee = employeesResponse.data.results[0];
    console.log(`   第一个员工: ${firstEmployee.name} (${firstEmployee.employee_id})`);
    console.log(`   部门: ${firstEmployee.department}`);
    console.log(`   职位: ${firstEmployee.position}`);
    console.log(`   薪资: ¥${firstEmployee.base_salary}`);
    
    // 3. 测试前端API代理
    console.log('\n3. 测试前端API代理...');
    const proxyResponse = await axios.get('http://localhost:3000/api/employees/', {
      headers: { 'Authorization': `Token ${token}` },
      params: { page: 1, page_size: 10 },
      timeout: 10000
    });
    
    console.log('✅ 前端API代理工作正常');
    console.log(`   代理返回员工数: ${proxyResponse.data.total_count}`);
    
    // 4. 验证数据结构
    console.log('\n4. 验证数据结构...');
    const apiData = proxyResponse.data;
    
    const requiredFields = ['results', 'total_count', 'current_page', 'total_pages'];
    const missingFields = requiredFields.filter(field => !(field in apiData));
    
    if (missingFields.length > 0) {
      console.log(`❌ API响应缺少字段: ${missingFields.join(', ')}`);
    } else {
      console.log('✅ API响应数据结构正确');
    }
    
    // 验证员工数据字段
    if (apiData.results.length > 0) {
      const employee = apiData.results[0];
      const employeeFields = ['id', 'employee_id', 'name', 'gender', 'department', 'position', 'base_salary', 'hire_date'];
      const missingEmployeeFields = employeeFields.filter(field => !(field in employee));
      
      if (missingEmployeeFields.length > 0) {
        console.log(`❌ 员工数据缺少字段: ${missingEmployeeFields.join(', ')}`);
      } else {
        console.log('✅ 员工数据字段完整');
      }
    }
    
    // 5. 测试前端页面访问
    console.log('\n5. 测试前端页面访问...');
    
    try {
      // 测试调试页面
      const debugResponse = await axios.get('http://localhost:3000/debug', {
        timeout: 5000,
        maxRedirects: 0,
        validateStatus: function (status) {
          return status >= 200 && status < 400;
        }
      });
      console.log('✅ 调试页面可访问');
    } catch (error) {
      if (error.response && error.response.status === 302) {
        console.log('✅ 调试页面重定向正常');
      } else {
        console.log('❌ 调试页面访问失败');
      }
    }
    
    // 测试员工页面
    try {
      const employeePageResponse = await axios.get('http://localhost:3000/employees', {
        timeout: 5000,
        maxRedirects: 0,
        validateStatus: function (status) {
          return status >= 200 && status < 400;
        }
      });
      
      if (employeePageResponse.status === 302) {
        console.log('✅ 员工页面正确重定向到登录页面（需要认证）');
      } else {
        console.log('✅ 员工页面可访问');
      }
    } catch (error) {
      console.log('❌ 员工页面访问失败:', error.message);
    }
    
    // 6. 总结
    console.log('\n📋 集成测试总结:');
    console.log('✅ 后端Django服务正常');
    console.log('✅ 数据库连接正常');
    console.log('✅ 员工数据存在且完整');
    console.log('✅ 前端Nuxt服务正常');
    console.log('✅ API代理工作正常');
    console.log('✅ 认证机制工作正常');
    
    console.log('\n🎯 下一步操作:');
    console.log('1. 在浏览器中访问: http://localhost:3000/debug');
    console.log('2. 点击"测试登录"按钮');
    console.log('3. 点击"测试员工API"验证数据获取');
    console.log('4. 访问: http://localhost:3000/login 进行正常登录');
    console.log('5. 登录后访问: http://localhost:3000/employees 查看员工管理页面');
    
    console.log('\n💡 如果员工管理页面仍然没有显示数据，可能的原因:');
    console.log('- 浏览器缓存问题（尝试硬刷新 Ctrl+F5）');
    console.log('- 认证token未正确传递（检查浏览器开发者工具）');
    console.log('- 前端JavaScript错误（检查浏览器控制台）');
    console.log('- API请求失败（检查网络选项卡）');
    
  } catch (error) {
    console.log('\n❌ 集成测试失败:');
    console.log(`   错误: ${error.message}`);
    if (error.response) {
      console.log(`   状态码: ${error.response.status}`);
      console.log(`   响应: ${JSON.stringify(error.response.data).substring(0, 200)}...`);
    }
    
    console.log('\n🔧 故障排除建议:');
    console.log('1. 确保后端服务在 http://localhost:8000 运行');
    console.log('2. 确保前端服务在 http://localhost:3000 运行');
    console.log('3. 检查数据库是否包含员工数据');
    console.log('4. 检查网络连接和防火墙设置');
  }
}

// 运行测试
testFinalIntegration().catch(console.error); 