import requests
import json
import jwt

from django.http  import JsonResponse
from django.views import View

from .models      import User, SocialPlatform
from my_settings  import SECRET_KEY, ALGORITHM

class KakaoSignInView(View):
    def post(self, request):
        try:  
            access_token = request.headers.get('Authorization', None)
    
            url        = 'https://kapi.kakao.com/v2/user/me'
            header     = {'Authorization' : f'Bearer {access_token}'}
            response   = requests.post(url, headers=header).json()
            
            user, created = User.objects.get_or_create(
                                user_code         = response['id'],
                                nickname          = response['properties']['nickname'],
                                profile_image_url = response['kakao_account']['profile']['profile_image_url'] if response['kakao_account']['profile'].get('profile_image_url') != None else None,
                                platform_id       = SocialPlatform.objects.get(platform='kakao').id
                            )
        
            access_token  = jwt.encode({'user_code' : user.user_code}, SECRET_KEY['secret'], ALGORITHM)
                
            return JsonResponse(
                    {
                        'MESSAGE'      : 'SUCCESS', 
                        'ACCESS_TOKEN' : access_token,
                        'IS_NEW'       : created
                    }, status=200
                )
            
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400) 
