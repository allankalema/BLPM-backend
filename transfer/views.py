from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Transfer
from .serializers import TransferSerializer

class CreateTransferView(APIView):
    """
    Create a new transfer record.
    """
    def post(self, request, *args, **kwargs):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            # Save the Transfer record
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateTransferView(APIView):
    """
    Update an existing transfer record.
    """
    def patch(self, request, pk, *args, **kwargs):
        try:
            transfer = Transfer.objects.get(pk=pk)
        except Transfer.DoesNotExist:
            return Response({"detail": "Transfer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransferSerializer(transfer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            transfer = Transfer.objects.get(pk=pk)
        except Transfer.DoesNotExist:
            return Response({"detail": "Transfer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransferSerializer(transfer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
