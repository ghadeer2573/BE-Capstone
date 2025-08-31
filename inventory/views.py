from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import InventoryItem, Customer, Sale, InventoryLog, Category
from .serializers import (
    InventoryItemSerializer, CustomerSerializer, SaleSerializer,
    InventoryLogSerializer, CategorySerializer, UserSerializer
)
from .permissions import IsOwnerOrAdmin
from django.contrib.auth.models import User

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__name']
    search_fields = ['name','description','dose']
    ordering_fields = ['name','quantity','price','date_added']

    def get_queryset(self):
        user = self.request.user
        qs = InventoryItem.objects.all()
        # If not staff, show only your items
        if user.is_authenticated and not user.is_staff:
            return qs.filter(owner=user)
        return qs

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def levels(self, request):
        "Return id, name, quantity for items (with filters/pagination applied)"
        qs = self.filter_queryset(self.get_queryset())
        data = qs.values('id','name','dose','quantity','price','category__name')
        return Response(data)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name','email','phone_number']

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().select_related('item','customer','sold_by')
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['date']

    def get_queryset(self):
        user = self.request.user
        # staff can see all; others may see only sales they made
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(sold_by=user)

class InventoryLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryLog.objects.all().select_related('item','changed_by')
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(item__owner=user)
