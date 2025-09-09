from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # 👈 add this
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 👇 define the home view
def home(request):
    return HttpResponse("Welcome to Pharmacy API 🚀")

urlpatterns = [
    path('', home),  # homepage route
    path('admin/', admin.site.urls),
    path('api/', include('inventory.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
