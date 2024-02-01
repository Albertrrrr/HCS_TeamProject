from django.utils.deprecation import MiddlewareMixin
from portal.models import User

class CustomUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                request.user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                request.user = None
        else:
            request.user = None