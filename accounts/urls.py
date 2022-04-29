from . import views
from django.urls import path 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',views.LoginAPI.as_view()),
    path('register/',views.CustomerRegistrationView.as_view()),
    path('logout/', views.LogoutVIEW.as_view(), name='logout'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('reset/', views.SendpasswordResetEmail.as_view(), name= 'reset'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name= 'password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name= 'password_reset_complete'),

    path('profile/', views.UserProfileUpdateView.as_view()),
]