from django.urls import path
from authen.views import (
    UserSignUp,
    UserSignIn,
    change_password,
    UserLogout,
    RequestPasswordRestEmail,
    SetNewPasswordView,
    UserProfile,
    CountrViews,
    GenderViews,

)

urlpatterns = [
    path('auth/signup', UserSignUp.as_view()),
    path('auth/sigin', UserSignIn.as_view()),
    path('auth/password', change_password),
    path('auth/logout', UserLogout.as_view()),
    path('auth/password/reset', RequestPasswordRestEmail.as_view()),
    path('auth/password/confirm', SetNewPasswordView.as_view()),
    path('auth/users', UserProfile.as_view()),
    path('country', CountrViews.as_view()),
    path('gender', GenderViews.as_view()),

]