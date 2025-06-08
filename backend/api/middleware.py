from django.utils.deprecation import MiddlewareMixin


class CSRFExemptMiddleware(MiddlewareMixin):
    """
    为API端点豁免CSRF检查的中间件
    """
    def process_request(self, request):
        # 如果请求路径以 /api/ 开头，则豁免CSRF检查
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None 