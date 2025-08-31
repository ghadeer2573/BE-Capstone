from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('drugs', views.InventoryItemViewSet, basename='drugs')
router.register('customers', views.CustomerViewSet)
router.register('sales', views.SaleViewSet)
router.register('logs', views.InventoryLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
