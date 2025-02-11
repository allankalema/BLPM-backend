from django.urls import path
from .views import CreateTransferView, UpdateTransferView

urlpatterns = [
    path('create/', CreateTransferView.as_view(), name='create_transfer'),  # URL for creating a transfer
    path('update/<int:pk>/', UpdateTransferView.as_view(), name='update_transfer'),  # URL for updating a transfer
]
