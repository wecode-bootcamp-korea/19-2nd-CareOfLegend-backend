import json
import jwt

from django            import forms
from django.test       import TestCase, Client
from django.core.files import File
from unittest.mock     import patch, MagicMock

from .models           import User, SocialPlatform
from my_settings       import SECRET_KEY, ALGORITHM

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
                'message'      : 'SUCCESS',
                'access_token' : f'{access_token}',
                'is_new'       : True
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
                'message'      : 'SUCCESS',
                'access_token' : f'{access_token}',
                'is_new'       : False
            }
        )

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
                    "message" : "KEY_ERROR"
                }
            )

class ProfileRegisterTest(TestCase):
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
        self.access_token = jwt.encode({'user_code':1234565432}, SECRET_KEY['secret'], ALGORITHM)
    
    def tearDown(self):
        User.objects.all().delete()
    
    @patch('users.views.boto3.client')
    def test_profile_register_success(self, mocked_s3client):
        client = Client()
            
        mock_file                      = MagicMock(spec=File)
        mock_file.name                 = 'test_profile.png'
        mocked_s3client.upload_fileobj = MagicMock()
        
        header   = {'HTTP_Authorization' : self.access_token}
        formdata = {'json' : 'test_nick', 'file' : mock_file}
            
        response = client.post(
                '/users/profile',
                formdata,
                **header
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {
                    "message" : "SUCCESS"
                }
        )
    
    @patch('users.views.boto3.client')
    def test_profile_register_json_key_error(self, mocked_s3client):
        client = Client()
            
        mock_file                      = MagicMock(spec=File)
        mock_file.name                 = 'test_profile.png'
        mocked_s3client.upload_fileobj = MagicMock()
        
        header   = {'HTTP_Authorization' : self.access_token}
        formdata = {'text' : 'test_nick', 'file' : mock_file}
            
        response = client.post(
                '/users/profile',
                formdata,
                **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message" : "KEY_ERROR"
                }
        )

    @patch('users.views.boto3.client')
    def test_profile_register_file_key_error(self, mocked_s3client):
        client = Client()
            
        mock_file                      = MagicMock(spec=File)
        mock_file.name                 = 'test_profile.png'
        mocked_s3client.upload_fileobj = MagicMock()
        
        header   = {'HTTP_Authorization' : self.access_token}
        formdata = {'json' : 'test_nick', 'image' : mock_file}
            
        response = client.post(
                '/users/profile',
                formdata,
                **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message" : "KEY_ERROR"
                }
        )

    def test_profile_show_success(self):
        client = Client()
        header   = {'HTTP_Authorization' : self.access_token}
        response = client.get(
            '/users/profile',
            **header
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {
                    "message" : "SUCCESS",
                    "results" : {
                        "nickname"          : "testkim",
                        "profile_image_url" : "http://www.careoflegend.co.kr"
                    }
                }
        )