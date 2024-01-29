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
from authen.views.view import CountrViews, GenderViews, UsersViws

urlpatterns = [
    path('auth/signup', UserSignUp.as_view()),
    path('auth/sigin', UserSignIn.as_view()),
    path('auth/password', change_password),
    path('auth/password/reset', RequestPasswordRestEmail.as_view()),
    path('auth/password/confirm', SetNewPasswordView.as_view()),
    path('auth/user', UserProfile.as_view()),
    path('auth/users', UsersViws.as_view()),
    path('country', CountrViews.as_view()),
    path('gender', GenderViews.as_view()),

]