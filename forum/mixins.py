from django.core.exceptions import PermissionDenied
class UserIsAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.role != 'admin' and self.request.user.role != 'moderator':
            raise PermissionDenied 
        return super().dispatch(request, *args, **kwargs)
    
    
