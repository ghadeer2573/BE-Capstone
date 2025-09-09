from django.urls import path
from django.http import HttpResponse

def inventory_home(request):
    return HttpResponse("Inventory API is working ✅")

urlpatterns = [
    path('', inventory_home),
]

from django.urls import path
from .views import ItemListCreateView, ItemDetailView

urlpatterns = [
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
