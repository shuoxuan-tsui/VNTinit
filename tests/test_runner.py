import time
import random
from playwright.sync_api import sync_playwright, expect
from report_generator import generate_html_report

BASE_URL = "http://localhost:3000"
# 为确保测试的独立性，使用动态的工号和电话
EMP_ID = f"EMP{random.randint(1000, 9999)}"
EMP_PHONE = f"138{random.randint(10000000, 99999999)}"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123" # 请根据实际密码修改

class TestRunner:
    def __init__(self, headless=True):
        self.results = []
        self.headless = headless
        self.page = None

    def run_test(self, test_case, name, test_func, *args):
        """通用测试执行器"""
        start_time = time.time()
        print(f"🚀 开始测试: [{test_case}] {name}")
        try:
            test_func(*args)
            duration = time.time() - start_time
            self.results.append({'test_case': test_case, 'name': name, 'status': '✅ PASSED', 'duration': duration})
            print(f"✅ 测试通过: [{test_case}] {name} (耗时: {duration:.2f}s)")
        except Exception as e:
            duration = time.time() - start_time
            error_message = str(e).splitlines()[0] # 获取更简洁的错误信息
            self.results.append({'test_case': test_case, 'name': name, 'status': '❌ FAILED', 'duration': duration, 'error': str(e)})
            print(f"❌ 测试失败: [{test_case}] {name} (耗时: {duration:.2f}s)\n   错误: {error_message}")
        finally:
            if self.page:
                self.page.wait_for_timeout(500) # 短暂等待，让UI反应

    def run_all_tests(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless, slow_mo=50)
            context = browser.new_context()
            self.page = context.new_page()

            # --- 认证模块测试 ---
            self.run_test('TC-AUTH-001', '成功登录', self._test_successful_login)
            self.run_test('TC-AUTH-002', '使用无效凭证登录', self._test_failed_login)
            self.run_test('TC-AUTH-003', '成功登出', self._test_logout)

            # 登出后需要重新登录以进行后续测试
            self._login()

            # --- 仪表盘模块测试 ---
            self.run_test('TC-DASH-001', '查看仪表盘统计', self._test_dashboard_stats)

            # --- 员工管理模块测试 ---
            self.run_test('TC-EMP-001', '查看员工列表', self._test_view_employee_list)
            self.run_test('TC-EMP-004', '成功添加新员工', self._test_add_employee)
            self.run_test('TC-EMP-002', '搜索新增的员工', self._test_search_employee)
            self.run_test('TC-EMP-003', '筛选员工', self._test_filter_employee)
            self.run_test('TC-EMP-005', '使用重复工号添加员工', self._test_add_duplicate_employee)
            self.run_test('TC-EMP-006', '快速编辑员工', self._test_edit_employee)
            self.run_test('TC-EMP-007', '删除员工', self._test_delete_employee)
            
            browser.close()
        
        generate_html_report(self.results)

    def _login(self, username=ADMIN_USER, password=ADMIN_PASS):
        """辅助登录函数"""
        self.page.goto(f"{BASE_URL}/login")
        self.page.get_by_placeholder("请输入用户名").fill(username)
        self.page.get_by_placeholder("请输入密码").fill(password)
        self.page.get_by_role("button", name="登录").click()
        expect(self.page.get_by_text(f"欢迎回来，{username}")).to_be_visible(timeout=10000)

    def _test_successful_login(self):
        self._login()

    def _test_failed_login(self):
        self.page.goto(f"{BASE_URL}/login")
        self.page.get_by_placeholder("请输入用户名").fill("wronguser")
        self.page.get_by_placeholder("请输入密码").fill("wrongpassword")
        self.page.get_by_role("button", name="登录").click()
        expect(self.page.get_by_text("用户名或密码错误")).to_be_visible()

    def _test_logout(self):
        if "login" in self.page.url:
             self._login()
        
        self.page.locator("button", has_text="admin").click()
        self.page.get_by_role("menuitem", name="登出").click()
        expect(self.page.get_by_role("heading", name="登录到您的账户")).to_be_visible()

    def _test_dashboard_stats(self):
        self.page.goto(f"{BASE_URL}/")
        expect(self.page.get_by_role("heading", name="仪表盘")).to_be_visible()
        # 验证总员工数卡片的值
        total_employees_card = self.page.locator("div:has-text('总员工数')").locator("dd")
        expect(total_employees_card).not_to_contain_text("NaN")
        card_text = total_employees_card.text_content()
        assert card_text.strip().isdigit(), f"仪表盘总员工数卡片内容 '{card_text}' 不是数字"

    def _test_view_employee_list(self):
        self.page.goto(f"{BASE_URL}/employees")
        expect(self.page.get_by_role("heading", name="员工管理")).to_be_visible()
        expect(self.page.locator("table tr")).to_have_count(lambda c: c > 1, timeout=10000)

    def _test_add_employee(self):
        self.page.goto(f"{BASE_URL}/employees/add")
        self.page.get_by_label("姓名").fill("测试用户")
        self.page.get_by_label("工号").fill(EMP_ID)
        self.page.get_by_label("职位").fill("测试工程师")
        self.page.get_by_label("部门").select_option(label="技术部")
        self.page.get_by_label("电话").fill(EMP_PHONE)
        self.page.get_by_label("入职日期").fill("2024-01-01")
        self.page.get_by_label("基础工资").fill("15000")
        self.page.get_by_role("button", name="确认添加").click()
        expect(self.page.get_by_text("员工添加成功")).to_be_visible(timeout=10000)
        expect(self.page.get_by_text(EMP_ID)).to_be_visible()

    def _test_search_employee(self):
        self.page.goto(f"{BASE_URL}/employees")
        self.page.get_by_placeholder("搜索姓名、工号、电话...").fill("测试用户")
        self.page.wait_for_timeout(1000) # 等待debounce
        expect(self.page.locator("table tbody tr")).to_have_count(1)
        expect(self.page.get_by_text("测试用户")).to_be_visible()

    def _test_filter_employee(self):
        self.page.goto(f"{BASE_URL}/employees")
        self.page.get_by_label("部门").select_option(label="技术部")
        self.page.wait_for_timeout(1000)
        all_rows = self.page.locator('table tbody tr').all()
        for row in all_rows:
            expect(row.locator('td').nth(2)).to_have_text("技术部")
        # 清空筛选
        self.page.get_by_label("部门").select_option(label="全部部门")

    def _test_add_duplicate_employee(self):
        self.page.goto(f"{BASE_URL}/employees/add")
        self.page.get_by_label("工号").fill(EMP_ID)
        self.page.get_by_label("姓名").fill("重复用户")
        self.page.get_by_label("职位").fill("测试工程师")
        self.page.get_by_label("部门").select_option(label="技术部")
        self.page.get_by_label("电话").fill("13900000001")
        self.page.get_by_label("入职日期").fill("2024-01-01")
        self.page.get_by_label("基础工资").fill("15000")
        self.page.get_by_role("button", name="确认添加").click()
        expect(self.page.get_by_text("该工号已存在")).to_be_visible()

    def _test_edit_employee(self):
        self.page.goto(f"{BASE_URL}/employees")
        row = self.page.locator(f"tr:has-text('{EMP_ID}')")
        row.get_by_role("button", name="编辑").click()
        
        modal = self.page.locator("div[role='dialog']")
        modal.get_by_label("职位").fill("高级测试工程师")
        modal.get_by_role("button", name="保存").click()

        expect(self.page.get_by_text("员工更新成功")).to_be_visible()
        expect(row.get_by_text("高级测试工程师")).to_be_visible()
    
    def _test_delete_employee(self):
        self.page.goto(f"{BASE_URL}/employees")
        row = self.page.locator(f"tr:has-text('{EMP_ID}')")
        
        row.get_by_role("button", name="删除").click()
        
        # 移除了 page.on('dialog')，因为它与新版UI的模态框确认方式冲突。
        # 直接等待并点击模态框中的确认删除按钮。
        confirm_button = self.page.locator("button:has-text('确认删除')")
        expect(confirm_button).to_be_visible(timeout=5000)
        confirm_button.click()

        expect(self.page.get_by_text("员工删除成功")).to_be_visible(timeout=5000)
        expect(self.page.get_by_text(EMP_ID)).not_to_be_visible()


if __name__ == "__main__":
    # 设置 headless=True 可以在无图形界面的环境中（如服务器、WSL）稳定运行测试
    runner = TestRunner(headless=True)
    runner.run_all_tests() 