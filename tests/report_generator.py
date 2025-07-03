import webbrowser
import os
from datetime import datetime

def generate_html_report(results):
    """根据测试结果生成HTML报告"""
    total_tests = len(results)
    passed_count = sum(1 for r in results if r['status'] == '✅ PASSED')
    failed_count = total_tests - passed_count
    pass_rate = (passed_count / total_tests) * 100 if total_tests > 0 else 0

    rows = ""
    for r in results:
        status_class = "passed" if r['status'] == '✅ PASSED' else "failed"
        error_details = r.get('error', '').replace('<', '&lt;').replace('>', '&gt;')
        
        # 为错误详情添加一个可折叠的区域
        error_html = f"""
        <details>
            <summary>查看详情</summary>
            <pre>{error_details}</pre>
        </details>
        """ if error_details else "无"

        rows += f"""
        <tr class="{status_class}">
            <td>{r['test_case']}</td>
            <td>{r['name']}</td>
            <td>{r['status']}</td>
            <td>{r['duration']:.2f}s</td>
            <td>{error_html}</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>VNTinit 黑盒测试报告</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Roboto', sans-serif; margin: 0; background-color: #f4f7f9; color: #333; }}
            .container {{ padding: 2rem; max-width: 1200px; margin: auto; }}
            header {{ background-color: #2c3e50; color: white; padding: 2rem; border-radius: 8px; margin-bottom: 2rem; text-align: center; }}
            header h1 {{ margin: 0; font-size: 2.5rem; }}
            header p {{ margin: 0.5rem 0 0; font-size: 1.1rem; opacity: 0.9; }}
            .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
            .card {{ background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }}
            .card h3 {{ margin: 0 0 0.5rem; color: #555; }}
            .card .value {{ font-size: 2rem; font-weight: 700; }}
            .passed .value {{ color: #2ecc71; }}
            .failed .value {{ color: #e74c3c; }}
            .total .value {{ color: #3498db; }}
            .rate .value {{ color: #f39c12; }}
            table {{ width: 100%; border-collapse: collapse; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden;}}
            th, td {{ padding: 1rem; text-align: left; border-bottom: 1px solid #e0e0e0; }}
            th {{ background-color: #34495e; color: white; font-weight: 500; }}
            tr:last-child td {{ border-bottom: none; }}
            tr.passed {{ background-color: #e8f5e9; }}
            tr.failed {{ background-color: #fce4e4; }}
            td:nth-child(3) {{ font-weight: bold; }}
            tr.passed td:nth-child(3) {{ color: #28a745; }}
            tr.failed td:nth-child(3) {{ color: #dc3545; }}
            details {{ cursor: pointer; }}
            pre {{ background-color: #eee; padding: 1rem; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>VNTinit 黑盒测试报告</h1>
                <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </header>

            <div class="summary">
                <div class="card total"><h3>总用例数</h3><p class="value">{total_tests}</p></div>
                <div class="card passed"><h3>通过</h3><p class="value">{passed_count}</p></div>
                <div class="card failed"><h3>失败</h3><p class="value">{failed_count}</p></div>
                <div class="card rate"><h3>通过率</h3><p class="value">{pass_rate:.2f}%</p></div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>用例编号</th>
                        <th>用例名称</th>
                        <th>状态</th>
                        <th>耗时</th>
                        <th>详情</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    report_path = os.path.join(os.path.dirname(__file__), 'test_report.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"测试报告已生成: {report_path}")
    webbrowser.open('file://' + os.path.realpath(report_path)) 