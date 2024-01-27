from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def login_permissions(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "The user is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        return func(self, request, *args, **kwargs)
    return wrapper
