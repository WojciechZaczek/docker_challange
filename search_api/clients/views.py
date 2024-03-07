from .models import Client
from rest_framework import viewsets
from .serializer import ClientSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=False, methods=['GET'])
    def get_client_by_pesel(self, request):
        pesel = request.query_params.get('pesel')
        try:
            client = Client.objects.get(pesel=pesel)
            serializer = self.get_serializer(client)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



