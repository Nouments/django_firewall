from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework import status

class ReceiveJSONDataView(APIView):
    @parser_classes([JSONParser])
    def post(self, request, *args, **kwargs):
        # Vérifier si le type de contenu est application/json
        if request.content_type != 'application/json':
            return Response({'error': 'Le type de contenu doit être application/json'}, status=status.HTTP_400_BAD_REQUEST)

        # Accéder aux données JSON à partir de la requête
        json_data = request.data

        # Faire quelque chose avec les données JSON, par exemple, les imprimer
        print("Données JSON reçues :", json_data)

        # Répondre avec un message JSON
        response_data = {'message': 'Données JSON reçues avec succès'}
        return Response(response_data, status=status.HTTP_200_OK)
