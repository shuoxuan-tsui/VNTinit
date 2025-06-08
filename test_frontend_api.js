// 测试前端API调用
const testEmployeeAPI = async () => {
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
      // 使用token获取员工数据
      const employeesResponse = await fetch('http://localhost:3003/api/employees/', {
        headers: {
          'Authorization': `Token ${loginData.data.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      const employeesData = await employeesResponse.json();
      console.log('Employees response:', {
        total_count: employeesData.total_count,
        results_length: employeesData.results?.length,
        first_employee: employeesData.results?.[0]
      });
    }
  } catch (error) {
    console.error('Error:', error);
  }
};

testEmployeeAPI(); 