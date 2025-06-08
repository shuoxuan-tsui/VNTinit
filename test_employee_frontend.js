const axios = require('axios');

async function testEmployeeFrontend() {
  console.log('🧪 测试员工管理前端功能...\n');

  try {
    // 1. 测试后端API直接访问
    console.log('1. 测试后端API登录...');
    const loginResponse = await axios.post('http://localhost:8000/api/auth/login/', {
      username: 'admin',
      password: 'admin123'
    });
    
    if (loginResponse.data.success) {
      console.log('✅ 后端登录成功');
      const token = loginResponse.data.data.token;
      console.log(`   Token: ${token.substring(0, 20)}...`);
      
      // 2. 测试员工API
      console.log('\n2. 测试员工API...');
      const employeesResponse = await axios.get('http://localhost:8000/api/employees/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      
      console.log('✅ 员工API响应成功');
      console.log(`   员工总数: ${employeesResponse.data.total_count}`);
      console.log(`   当前页员工数: ${employeesResponse.data.results.length}`);
      console.log(`   第一个员工: ${employeesResponse.data.results[0]?.name} (${employeesResponse.data.results[0]?.employee_id})`);
      
      // 3. 测试前端服务
      console.log('\n3. 测试前端服务...');
      const frontendResponse = await axios.get('http://localhost:3000', {
        maxRedirects: 0,
        validateStatus: function (status) {
          return status >= 200 && status < 400; // 允许重定向
        }
      });
      
      if (frontendResponse.status === 302) {
        console.log('✅ 前端服务运行正常 (重定向到登录页面)');
        console.log(`   重定向到: ${frontendResponse.headers.location}`);
      } else {
        console.log('✅ 前端服务运行正常');
      }
      
      // 4. 测试前端API代理
      console.log('\n4. 测试前端API代理...');
      try {
        const proxyResponse = await axios.get('http://localhost:3000/api/employees/', {
          headers: {
            'Authorization': `Token ${token}`
          },
          timeout: 10000
        });
        console.log('✅ 前端API代理工作正常');
        console.log(`   代理返回员工数: ${proxyResponse.data.total_count || proxyResponse.data.results?.length || 0}`);
      } catch (proxyError) {
        console.log('❌ 前端API代理测试失败:');
        console.log(`   错误: ${proxyError.message}`);
        if (proxyError.response) {
          console.log(`   状态码: ${proxyError.response.status}`);
          console.log(`   响应: ${JSON.stringify(proxyError.response.data).substring(0, 200)}...`);
        }
      }
      
    } else {
      console.log('❌ 后端登录失败');
      console.log(`   响应: ${JSON.stringify(loginResponse.data)}`);
    }
    
  } catch (error) {
    console.log('❌ 测试过程中发生错误:');
    console.log(`   错误: ${error.message}`);
    if (error.response) {
      console.log(`   状态码: ${error.response.status}`);
      console.log(`   响应: ${JSON.stringify(error.response.data).substring(0, 200)}...`);
    }
  }
  
  console.log('\n📋 测试总结:');
  console.log('- 后端Django服务应该在 http://localhost:8000 运行');
  console.log('- 前端Nuxt服务应该在 http://localhost:3000 运行');
  console.log('- 数据库应该包含员工数据');
  console.log('- 前端需要先登录才能访问员工数据');
  console.log('\n💡 如果前端无法显示数据，请检查:');
  console.log('1. 浏览器控制台是否有错误');
  console.log('2. 网络请求是否成功');
  console.log('3. 认证token是否正确传递');
  console.log('4. API响应数据结构是否匹配');
}

// 运行测试
testEmployeeFrontend().catch(console.error); 