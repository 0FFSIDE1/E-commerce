import threading

_thread_locals = threading.local()

def get_current_request():
    """Get the request from thread-local storage."""
    return getattr(_thread_locals, "request", None)

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        return response
