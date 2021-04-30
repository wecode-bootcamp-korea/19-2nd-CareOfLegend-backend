import json
import jwt

from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

from .models       import User, SocialPlatform
from my_settings   import SECRET_KEY, ALGORITHM

class KakaoSignInTest(TestCase):
    def setUp(self):
        SocialPlatform.objects.create(
            id       = 1,
            platform = 'kakao'
        )
        User.objects.create(
            id                = 1,
            user_code         = 1234565432,
            nickname          = 'testkim',
            profile_image_url = 'http://www.careoflegend.co.kr',
            platform          = SocialPlatform.objects.get(id = 1)
        )
    
    def tearDown(self):
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_kakao_new_user_login_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id" : 134565432,
                    "properties" : {
                        "nickname" : "testlee"
                    },
                    "kakao_account" : {
                        "profile" : {
                            "profile_image_url" : 
                            "http://www.wecode.co.kr"
                        }
                    }
                }
        
        mocked_requests.post = MagicMock(return_value = MockedResponse())
        
        header   = {'Authorization':'TEST_ACCESS_TOKEN'}
        response = client.post(
             '/users/kakao-login',
             content_type = 'application/json',
             **header
        )
        
        access_token = jwt.encode({'user_code':134565432}, SECRET_KEY['secret'], ALGORITHM)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'MESSAGE'      : 'SUCCESS',
                'ACCESS_TOKEN' : f'{access_token}',
                'IS_NEW'       : True
            }
        )

    @patch('users.views.requests')
    def test_kakao_user_login_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id" : 1234565432,
                    "properties" : {
                        "nickname" : "testkim"
                    },
                    "kakao_account" : {
                        "profile" : {
                            "profile_image_url" : 
                            "http://www.careoflegend.co.kr"
                        }
                    }
                }
        
        mocked_requests.post = MagicMock(return_value = MockedResponse())
        
        header   = {'Authorization':'TEST_ACCESS_TOKEN'}
        response = client.post(
             '/users/kakao-login',
             content_type = 'application/json',
             **header
        )
        
        access_token = jwt.encode({'user_code':1234565432}, SECRET_KEY['secret'], ALGORITHM)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'MESSAGE'      : 'SUCCESS',
                'ACCESS_TOKEN' : f'{access_token}',
                'IS_NEW'       : False
            }
        )

    # @patch('users.views.requests')
    def test_kakao_login_key_error(self):
        client = Client()
        
        header = {}
        
        response = client.post(
            '/users/kakao-login',
            content_type = 'application/json',
            **header
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "MESSAGE" : "KEY_ERROR"
                }
            )
