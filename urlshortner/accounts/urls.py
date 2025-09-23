from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify/', views.LoginVerifyView.as_view(), name='verify'),
    path('complete-register/', views.CompleteRegisterView.as_view(), name='complete-register'),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
