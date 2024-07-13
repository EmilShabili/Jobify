from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path("activation/<uuid>/", views.ActivationView.as_view(), name="activation"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),
    path("password-change/<uuid>/", views.ChangePasswordView.as_view(), name="password-change"),
    path("reset-password-complete/<uuid>/", views.ResetPasswordCompleteView.as_view(), name="reset_password_complete"),
]
