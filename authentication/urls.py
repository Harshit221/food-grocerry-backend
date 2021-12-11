from django.contrib import admin
from django.urls import path, include
import authentication.views as views
from django.urls import include
# from django.contrib.auth import views as authView

urlpatterns = [
    path('customer/register', views.CreateCustomer.as_view()),
    path('staff/register', views.CreateStaff.as_view()),
    path('token', views.ObtainAuthToken.as_view(), name='token'),
    path('logout', views.LogoutView.as_view()),
    path('profile', views.ProfileView.as_view())
]