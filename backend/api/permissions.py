from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    管理员可以进行所有操作，普通用户只能读取
    """
    def has_permission(self, request, view):
        # 读取权限对所有认证用户开放
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # 写入权限只对管理员开放
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or 
            request.user.groups.filter(name='Admin').exists()
        )


class IsAdminUser(permissions.BasePermission):
    """
    只有管理员可以访问
    the groups relationship is many-to-many relationship.
    the is IsAdminUser class defined by myself.
    the request is 
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or 
            request.user.groups.filter(name='Admin').exists()
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    只有资源所有者或管理员可以访问
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # 管理员可以访问所有资源
        if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
            return True
        # # check if the owner of resource.
        # if hasattr(obj, 'user') and obj.user:
        #     return obj.user == request.user
        
        # # for related objects (like salaryRecord)
        # if hasattr(obj, 'employee') and hasattr(obj.employee, 'user') and obj.employee.user:
        #     return obj.employee.user == request.user
        
        # 检查是否为资源所有者（需要在视图中实现具体逻辑）
        return False


class IsSalaryOwnerOrAdmin(permissions.BasePermission):
    """
    只有薪资记录所有者或管理员可以访问
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # 管理员可以访问所有薪资记录
        if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
            return True
        
        # if hasattr(obj, 'employee') and hasattr(obj.employee, 'user')
        # 员工只能访问自己的薪资记录
        # 这里需要建立User和Employee的关联关系
        # 暂时返回False，需要在实际项目中根据业务逻辑调整
        return False 