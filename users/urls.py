from django.urls import path

from .views      import KakaoSignInView, ProfileRegisterView

urlpatterns = [
        path('/kakao-login', KakaoSignInView.as_view()),
        path('/profile', ProfileRegisterView.as_view())
        ]
