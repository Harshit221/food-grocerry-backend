from django.contrib import admin
from django.urls import path, include
import authentication.views as views
from django.urls import include
from django.contrib.auth import views as authView

urlpatterns = [
    path('customer/',include('django.contrib.auth.urls')),
    path('customer/register', views.CreateCustomer.as_view()),
    # path('admin/login', ),
    # path('admin/register', ),
    # path('employee/login', ),
    # path('employee/register', )
]
# {"user": {"contact_no": "+919925497584", "first_name": "harshit", "password": "12345678", "last_name": "vaghani", "email": "fake@mail.com"}, "address": "ascascascas"}