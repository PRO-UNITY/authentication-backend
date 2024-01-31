from django.urls import path
from authen.views.auth_views import (
    UserSignIn,
    UserSignUp,
    UserProfile,
)
from authen.views.forget_password import (
    RequestPasswordRestEmail,
    SetNewPasswordView,
    change_password,

)
from authen.views.view import UsersViws

urlpatterns = [
    path('signup', UserSignUp.as_view()),
    path('sigin', UserSignIn.as_view()),
    path('password', change_password),
    path('password/reset', RequestPasswordRestEmail.as_view()),
    path('password/confirm', SetNewPasswordView.as_view()),
    path('user', UserProfile.as_view()),
    path('users', UsersViws.as_view()),
]