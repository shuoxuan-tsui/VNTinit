const puppeteer = require('puppeteer');

async function testFrontendLogin() {
  console.log('🧪 测试前端登录和员工页面...\n');

  let browser;
  try {
    // 启动浏览器
    browser = await puppeteer.launch({
      headless: false, // 设置为false可以看到浏览器操作
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // 监听控制台消息
    page.on('console', msg => {
      console.log(`浏览器控制台: ${msg.text()}`);
    });
    
    // 监听网络请求
    page.on('response', response => {
      if (response.url().includes('/api/')) {
        console.log(`API请求: ${response.status()} ${response.url()}`);
      }
    });
    
    // 1. 访问前端首页
    console.log('1. 访问前端首页...');
    await page.goto('http://localhost:3000', { waitUntil: 'networkidle2' });
    
    // 检查是否重定向到登录页面
    const currentUrl = page.url();
    if (currentUrl.includes('/login')) {
      console.log('✅ 正确重定向到登录页面');
      
      // 2. 填写登录表单
      console.log('2. 填写登录表单...');
      await page.waitForSelector('#username');
      await page.type('#username', 'admin');
      await page.type('#password', 'admin123');
      
      // 3. 提交登录
      console.log('3. 提交登录...');
      await page.click('button[type="submit"]');
      
      // 等待登录完成
      await page.waitForNavigation({ waitUntil: 'networkidle2' });
      
      const loginUrl = page.url();
      if (loginUrl === 'http://localhost:3000/' || loginUrl === 'http://localhost:3000') {
        console.log('✅ 登录成功，重定向到首页');
        
        // 4. 访问员工管理页面
        console.log('4. 访问员工管理页面...');
        await page.goto('http://localhost:3000/employees', { waitUntil: 'networkidle2' });
        
        // 等待页面加载
        await page.waitForTimeout(3000);
        
        // 检查页面内容
        const pageTitle = await page.$eval('h1', el => el.textContent);
        console.log(`页面标题: ${pageTitle}`);
        
        // 检查是否有员工数据
        const employeeRows = await page.$$('tbody tr');
        console.log(`员工数据行数: ${employeeRows.length}`);
        
        if (employeeRows.length > 0) {
          console.log('✅ 员工数据加载成功');
          
          // 获取第一行员工数据
          const firstRowData = await page.evaluate(() => {
            const firstRow = document.querySelector('tbody tr');
            if (firstRow) {
              const cells = firstRow.querySelectorAll('td');
              return Array.from(cells).map(cell => cell.textContent.trim()).slice(0, 5);
            }
            return [];
          });
          
          if (firstRowData.length > 0) {
            console.log(`第一个员工数据: ${firstRowData.join(' | ')}`);
          }
        } else {
          console.log('❌ 没有找到员工数据');
          
          // 检查是否有错误消息
          const errorMessage = await page.$eval('body', el => el.textContent).catch(() => '');
          if (errorMessage.includes('error') || errorMessage.includes('错误')) {
            console.log('页面可能有错误信息');
          }
        }
        
        // 5. 检查统计数据
        console.log('5. 检查统计数据...');
        const totalEmployees = await page.$eval('body', el => {
          const totalElement = el.querySelector('dd');
          return totalElement ? totalElement.textContent.trim() : '未找到';
        }).catch(() => '未找到');
        
        console.log(`总员工数显示: ${totalEmployees}`);
        
      } else {
        console.log('❌ 登录失败，未重定向到首页');
        console.log(`当前URL: ${loginUrl}`);
      }
      
    } else {
      console.log('❌ 未重定向到登录页面');
      console.log(`当前URL: ${currentUrl}`);
    }
    
  } catch (error) {
    console.error('❌ 测试过程中发生错误:', error.message);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
  
  console.log('\n📋 测试完成');
  console.log('💡 如果测试失败，请检查:');
  console.log('1. 前端服务是否在 http://localhost:3000 运行');
  console.log('2. 后端服务是否在 http://localhost:8000 运行');
  console.log('3. 数据库是否包含员工数据');
  console.log('4. 浏览器控制台是否有错误信息');
}

// 运行测试
testFrontendLogin().catch(console.error); 