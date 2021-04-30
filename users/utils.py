import jwt

from django.http import JsonResponse

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, SECRET_KEY['secret'], ALGORITHM)
            request.user = User.objects.get(user_code=payload['user_code'])

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE' : 'UNAUTHORIZED_TOKEN'}, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=401)

    return wrapper