from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls'))
]
# {"contact_no": "+919925497584", "first_name": "harshit", "password": "12345678"}