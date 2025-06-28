from django.urls import path
from django.http import JsonResponse
from . import views
from . import auth_views

def api_info(request):
    """API信息视图"""
    return JsonResponse({
        'message': '企业管理系统 API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'auth': {
                'login': '/api/auth/login/',
                'register': '/api/auth/register/',
                'logout': '/api/auth/logout/',
                'user': '/api/auth/user/',
                'change_password': '/api/auth/change-password/',
                'check': '/api/auth/check/'
            },
            'dashboard': {
                'summary_stats': '/api/dashboard/summary-stats/',
                'department_distribution': '/api/dashboard/department-distribution/'
            },
            'departments': {
                'list': '/api/departments/',
                'detail': '/api/departments/{id}/',
                'create': '/api/departments/',
                'update': '/api/departments/{id}/',
                'delete': '/api/departments/{id}/'
            },
            'employees': {
                'list': '/api/employees/',
                'detail': '/api/employees/{id}/',
                'salary_history': '/api/employees/{employee_id}/salary/'
            },
            'salaries': {
                'list': '/api/salaries/',
                'detail': '/api/salaries/{id}/',
                'calculate': '/api/salaries/calculate_and_create/',
                'print': '/api/salaries/{record_id}/print_view/',
                'stats': '/api/salaries/stats/',
                'export': '/api/salaries/export/'
            }
        }
    })

urlpatterns = [
    # API信息
    path('', api_info, name='api_info'),
    
    # 认证相关
    path('auth/login/', auth_views.LoginView.as_view(), name='api_login'),
    path('auth/register/', auth_views.RegisterView.as_view(), name='api_register'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='api_logout'),
    path('auth/user/', auth_views.CurrentUserView.as_view(), name='current_user'),
    path('auth/change-password/', auth_views.ChangePasswordView.as_view(), name='change_password'),
    path('auth/check/', auth_views.check_auth_view, name='check_auth'),
    
    # 仪表盘统计
    path('dashboard/summary-stats/', views.dashboard_summary_stats, name='dashboard_summary_stats'),
    path('dashboard/department-distribution/', views.dashboard_department_distribution, name='dashboard_department_distribution'),
    
    # 部门管理
    path('departments/', views.DepartmentListCreateView.as_view(), name='department_list_create'),
    path('departments/<uuid:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    
    # 员工管理
    path('employees/', views.EmployeeListCreateView.as_view(), name='employee_list_create'),
    path('employees/<uuid:id>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/<str:employee_id>/salary/', views.employee_salary_history_view, name='employee_salary_history'),
    
    # 薪资管理
    path('salaries/', views.SalaryRecordListView.as_view(), name='salary_list'),
    path('salaries/<uuid:id>/', views.SalaryRecordDetailView.as_view(), name='salary_detail'),
    path('salaries/calculate_and_create/', views.calculate_salary_view, name='calculate_salary'),
    path('salaries/<uuid:record_id>/print_view/', views.salary_print_view, name='salary_print'),
    path('salaries/stats/', views.salary_stats_view, name='salary_stats'),
    path('salaries/export/', views.salary_export_view, name='salary_export'),
    path('salaries/generate/', views.generate_salaries_view, name='generate_salaries'),
    path('salaries/calculate/<uuid:employee_id>/', views.calculate_salary_by_employee_view, name='calculate_salary_by_employee'),
    
    # # RAG知识库管理
    # path('knowledge/documents/', views.KnowledgeDocumentListCreateView.as_view(), name='knowledge_document_list_create'),
    # path('knowledge/documents/<uuid:pk>/', views.KnowledgeDocumentDetailView.as_view(), name='knowledge_document_detail'),
    # path('knowledge/upload/', views.upload_document_view, name='upload_document'),
    # path('knowledge/search/', views.search_documents_view, name='search_documents'),
    
    # # RAG聊天功能
    # path('chat/sessions/', views.ChatSessionListCreateView.as_view(), name='chat_session_list_create'),
    # path('chat/sessions/<uuid:pk>/', views.ChatSessionDetailView.as_view(), name='chat_session_detail'),
    # path('chat/sessions/<uuid:session_id>/messages/', views.chat_session_messages_view, name='chat_session_messages'),
    # path('chat/', views.chat_view, name='chat'),
    
    # # RAG系统管理
    # path('rag/stats/', views.rag_system_stats_view, name='rag_system_stats'),
] 