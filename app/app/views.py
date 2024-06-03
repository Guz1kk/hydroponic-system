from app.models import System, Measurement
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from app.serializers import SystemsSerializer, MeasurementSerializer, SingleSystemSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SystemsView(APIView):
    """ All systems view """
    
    @swagger_auto_schema(
        operation_description='Get all systems data',
        responses={200:SystemsSerializer(many=True)}
    )
    def get(self, request) -> JsonResponse:
        """ All system get """
        user = self.request.user
        systems = System.objects.filter(user=user)
        response = SystemsSerializer(systems, many=True)
        return JsonResponse(response.data, safe=False)

    @swagger_auto_schema(
        operation_description='Add systems',
        responses={201:'Successfully created'},
        request_body=SystemsSerializer,
    )
    def post(self, request) -> HttpResponse:
        serializer = SystemsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=201)
        return HttpResponse(serializer.errors, status=400)
    
    

class SingleSystemView(APIView):
    """ Single system view """
    
    @swagger_auto_schema(
        operation_description='Get single system data with last 10 measurements',
        responses={404:'Object not found',
                   200: SingleSystemSerializer(many=False)}
    )
    def get(self, request, systemID:int) -> JsonResponse:
        """Single system indo

        Args:
            systemID (int): system id

        Returns:
            HttpResponse: HTTP 404 if object not found
            JsonResponse: system info JSON
        """
        user = self.request.user
        system = get_object_or_404(System, pk=systemID, user=user)
        response = SingleSystemSerializer(system, many=False)
        return JsonResponse(response.data, safe=False)
    
    @swagger_auto_schema(
        operation_description='Delete system',
        responses={204:'Successfull delete',
                   404:'Object not found'},
        manual_parameters=[
            openapi.Parameter(
                'systemID',
                openapi.IN_PATH,
                description="System ID",
                type=openapi.TYPE_INTEGER
            )
        ],
        security=[{'Bearer': []}]
    )
    def delete(self, request, systemID:int) -> HttpResponse:
        """_summary_

        Args:
            systemID (int): system id

        Returns:
            HttpResponse: HTTP 204 - successfull delete
                          HTTP 404 - object not found
        """
        user=self.request.user
        system = get_object_or_404(System, pk=systemID, user=user)
        system.delete()
        return HttpResponse(status=204)
    

class MeasurementView(APIView):
    """ Measurement view """
    
    @swagger_auto_schema(
        operation_description='Get system measurements',
        responses={200: MeasurementSerializer,
                   404:'Object not found'}
    )
    def get(self, request, systemID:int) -> JsonResponse:
        user = self.request.user
        system = get_object_or_404(System, pk=systemID, user=user)
        measurements = Measurement.objects.filter(system=system)
        response = MeasurementSerializer(measurements, many=True)
        return JsonResponse(response.data, safe=False)
    
    @swagger_auto_schema(
        operation_description='Add measurement',
        request_body=MeasurementSerializer,
        responses={201:'Successfully added',
                   400:'Bad request'}
    )
    def post(self, request, sytemID:int) -> HttpResponse:
        serializer = MeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=201)
        return HttpResponse(status=400)