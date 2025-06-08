// 测试仪表盘API调用
const testDashboardAPI = async () => {
  try {
    // 首先登录获取token
    const loginResponse = await fetch('http://localhost:3003/api/auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'admin', password: 'admin123' })
    });
    
    const loginData = await loginResponse.json();
    console.log('Login response:', loginData);
    
    if (loginData.success && loginData.data.token) {
      // 测试仪表盘统计API
      const statsResponse = await fetch('http://localhost:3003/api/dashboard/summary-stats/', {
        headers: {
          'Authorization': `Token ${loginData.data.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      const statsData = await statsResponse.json();
      console.log('Dashboard stats response:', statsData);
      
      // 测试部门分布API
      const deptResponse = await fetch('http://localhost:3003/api/dashboard/department-distribution/', {
        headers: {
          'Authorization': `Token ${loginData.data.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      const deptData = await deptResponse.json();
      console.log('Department distribution response:', deptData);
      
    } else {
      console.error('Login failed:', loginData);
    }
  } catch (error) {
    console.error('Error:', error);
  }
};

testDashboardAPI(); 