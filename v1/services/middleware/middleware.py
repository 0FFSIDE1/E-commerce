from threading import local

_request_storage = local()

def get_current_request():
    """
    Retrieve the current request stored in thread-local storage.

    Returns:
        HttpRequest object or None if not set.
    """
    return getattr(_request_storage, 'request', None)

class CurrentRequestMiddleware:
    """
    Middleware to store the current request in thread-local storage.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_storage.request = request
        response = self.get_response(request)
        return response
