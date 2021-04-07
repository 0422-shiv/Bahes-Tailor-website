# Import some useful packages.
from django.urls import path
from django.contrib.auth.models import User, auth
from . import views

# Define urls for User Application function.
urlpatterns = [
path('login', views.login_user.as_view(), name="login"),
path('logout', views.logout_request, name="logout"),
path('registration', views.CreateUserView.as_view(), name="CreateUserView"),
path('user-type', views.UserTypes.as_view(), name="UserType"),
path('verify/<int:id>', views.OtpViewPage.as_view(), name="OtpViewPage"),
###########forgot password urls################################
path('forgot-password', views.ForgotPassword.as_view(), name="ForgotPassword"),
path('forgot-password-otp/<str:email>', views.ForgotPasswordOtp.as_view(), name="ForgotPasswordOtp"),
path('check-reset/<str:otp>/<str:email>', views.PasswordReset.as_view(), name="PasswordReset"),
path('newpassword-done', views.NewPasswordDone.as_view(), name="NewPasswordDone"),
###########forgot password urls end################################

]