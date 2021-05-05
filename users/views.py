import requests
import json
import jwt
import boto3

from django.http  import JsonResponse
from django.views import View

from .models      import User, SocialPlatform
from .utils       import login_decorator
from my_settings  import SECRET_KEY, ALGORITHM, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME, DEFAULT_IMAGE_URL

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
                        'message'      : 'SUCCESS', 
                        'access_token' : access_token,
                        'is_new'       : created
                    }, status=200
                )
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400) 


class ProfileRegisterView(View):
    @login_decorator
    def post(self, request):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        try:
            user       = request.user
            nickname   = request.POST['json']
            image_file = request.FILES['file']
            
            key      = str(user.user_code)
            location = s3_client.get_bucket_location(Bucket=AWS_S3_BUCKET_NAME)['LocationConstraint']
                                
            s3_client.upload_fileobj(
                                image_file, 
                                AWS_S3_BUCKET_NAME,
                                f'user-profile-image/{key}/{image_file.name}',
                                ExtraArgs={
                                    "ContentType": image_file.content_type
                                }
                            )
            
            url      = f'http://{AWS_S3_BUCKET_NAME}.s3.{location}.amazonaws.com/user-profile-image/{key}/{image_file.name}'
            
            User.objects.filter(user_code=user.user_code).update(nickname=nickname, profile_image_url=url)
            
            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    @login_decorator
    def get(self, request):
        try:
            user = request.user
        
            user_profile = {
                "nickname"          : user.nickname,
                "profile_image_url" : user.profile_image_url if user.profile_image_url else DEFAULT_IMAGE_URL
            }

            return JsonResponse({'message' : 'SUCCESS', 'results' : user_profile}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

            