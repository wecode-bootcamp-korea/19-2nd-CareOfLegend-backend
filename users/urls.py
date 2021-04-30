from django.urls import path

from .views      import KakaoSignInView

urlpatterns = [
        path('/kakao-login', KakaoSignInView.as_view()),
        ]
