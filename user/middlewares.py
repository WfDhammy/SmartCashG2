from django.http import HttpResponseForbidden

class VerifyRequestMiddleware:
    """Middleware to check if the user verification status is True"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and not getattr(user, "verified", False):
            return HttpResponseForbidden("Your account is not verified. Please verify your email.")

        response = self.get_response(request)
        return response
