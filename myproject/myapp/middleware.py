# your_app/middleware.py
from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path == '/logout/':  # Adjust path as needed
            response['Cache-Control'] = 'no-store'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
