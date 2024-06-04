from app.models import System, Measurement
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from app.serializers import SystemsSerializer, MeasurementSerializer, SingleSystemSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.paginator import Paginator


class SystemsView(APIView):
    """ All systems view """
    
    DEFAULT_SORT_BY = 'name'
    DEFAULT_SORT_ORDER = 'asc'
    
    sort_by_param = openapi.Parameter('sort_by', openapi.IN_QUERY,
                                    description='Field on sort by',
                                    type=openapi.TYPE_STRING)
    order_by_param = openapi.Parameter('sort_order', openapi.IN_QUERY,
                                    description='Sort order ("asc" or "desc")',
                                    type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(
        operation_description='GET all systems data',
        responses={200:SystemsSerializer(many=True),},
        manual_parameters=[sort_by_param, order_by_param],
    )
    def get(self, request) -> JsonResponse:
        """ All system get """
        sort_by = request.query_params.get('sort_by',self.DEFAULT_SORT_BY)
        order_by = '-' if request.query_params.get('sort_order', self.DEFAULT_SORT_ORDER)=='desc' else ''
        
        user = self.request.user
        systems = System.objects.filter(user=user)
        systems = systems.order_by(f"{order_by}{sort_by}")
        response = SystemsSerializer(systems, many=True)
        return JsonResponse(response.data, safe=False)

    @swagger_auto_schema(
        operation_description='Add systems',
        responses={201:'Successfully created'},
        request_body=SystemsSerializer,
    )
    def post(self, request) -> HttpResponse:
        """Add system

        Returns:
            HttpResponse: 201 Successfully added
                          400 Bad request
        """
        serializer = SystemsSerializer(data=request.data,
                                       context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=201)
        return HttpResponse(serializer.errors, status=400)
    
    

class SingleSystemView(APIView):
    """ Single system view """
    
    @swagger_auto_schema(
        operation_description='Get single system data with last 10 measurements',
        responses={404:'Object not found',
                   200: SingleSystemSerializer(many=False)},
        manual_parameters=[
            openapi.Parameter(
                'systemID',
                openapi.IN_PATH,
                description="System ID",
                type=openapi.TYPE_INTEGER
            )
        ],
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
        operation_description='Update system',
        responses={200:'Successfull update',
                   404:'Object not found'},
        manual_parameters=[
            openapi.Parameter(
                'systemID',
                openapi.IN_PATH,
                description="System ID",
                type=openapi.TYPE_INTEGER
            )
        ],
        request_body=SingleSystemSerializer,
        security=[{'Bearer': []}]
    )
    def patch(self, request, systemID:int) -> JsonResponse:
        """Update system

        Args:
            systemID (int): system id

        Returns:
            JsonResponse: HTTP 200 - successful update
                          HTTP 404 - object not found
        """
        user=self.request.user
        system = get_object_or_404(System, pk=systemID, user=user)
        serializer = SystemsSerializer(system, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
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
        """Delete system

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
    
    DEFAULT_SORT_BY = "id"
    DEFAULT_SORT_ORDER = "asc"
    DEFAULT_LIMIT = 50
    DEFAULT_OFFSET = 1
    DEFAULT_FILTER_PARAM = ''
    DEFAULT_START_VALUE_PARAM = ''
    DEFAULT_END_VALUE_PARAM = ''
    
    sort_by_param = openapi.Parameter('sort_by', openapi.IN_QUERY,
                                    description='Field on sort by',
                                    type=openapi.TYPE_STRING)
    order_by_param = openapi.Parameter('sort_order', openapi.IN_QUERY,
                                    description='Sort order ("asc" or "desc")',
                                    type=openapi.TYPE_STRING)
    limit_param = openapi.Parameter('limit', openapi.IN_QUERY,
                                    description='Max objects on page',
                                    type=openapi.TYPE_INTEGER)
    offset_param = openapi.Parameter('offset', openapi.IN_QUERY,
                                    description='Page number',
                                    type=openapi.TYPE_INTEGER)
    filter_param = openapi.Parameter('filter', openapi.IN_QUERY,
                                    description='Field to filter by',
                                    type=openapi.TYPE_STRING)
    start_value_param = openapi.Parameter('start_value', openapi.IN_QUERY,
                                    description='Start value for the filter',
                                    type=openapi.TYPE_STRING)
    end_value_param = openapi.Parameter('end_value', openapi.IN_QUERY,
                                    description='End value for the filter',
                                    type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(
        operation_description='Get system measurements',
        responses={200: MeasurementSerializer,
                   404:'Object not found'},
        manual_parameters=[sort_by_param, order_by_param, limit_param,
                           offset_param, filter_param, start_value_param,
                           end_value_param,],
    )
    def get(self, request, systemID:int) -> JsonResponse:
        """Get measurements

        Args:
            systemID (int): system id

        Returns:
            JsonResponse: Measurements
        """
        sort_by = request.query_params.get('sort_by',self.DEFAULT_SORT_BY)
        order_by = '-' if request.query_params.get('sort_order', self.DEFAULT_SORT_ORDER)=='desc' else ''
        limit = request.query_params.get('limit', self.DEFAULT_LIMIT)
        offset = request.query_params.get('offset', self.DEFAULT_OFFSET)
        filter_param = request.query_params.get('filter', self.DEFAULT_FILTER_PARAM)
        start_value_param = request.query_params.get('start_value', self.DEFAULT_START_VALUE_PARAM)
        end_value_param = request.query_params.get('end_value', self.DEFAULT_END_VALUE_PARAM)

        user = self.request.user
        system = get_object_or_404(System, pk=systemID, user=user)
        measurements = Measurement.objects.filter(system=system)
        
        if filter_param and (start_value_param or end_value_param):
            filter_kwargs = {}
            if start_value_param:
                filter_kwargs[f"{filter_param}__gte"] = start_value_param
            if end_value_param:
                filter_kwargs[f"{filter_param}__lte"] = end_value_param
            measurements = measurements.filter(**filter_kwargs)
        
        measurements = measurements.order_by(f"{order_by}{sort_by}")
        paginator = Paginator(measurements, limit)
        page = paginator.page(offset)
        response = MeasurementSerializer(page, many=True)
        return JsonResponse(response.data, safe=False)
    
    @swagger_auto_schema(
        operation_description='Add measurement',
        request_body=MeasurementSerializer,
        responses={201:'Successfully added',
                   400:'Bad request'}
    )
    def post(self, request, systemID:int) -> HttpResponse:
        """Add measurement

        Args:
            systemID (int): system id

        Returns:
            HttpResponse: 201 Successfully added
                          400 Bad request
        """
        request.data['system'] = systemID
        serializer = MeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=201)
        return HttpResponse(status=400)