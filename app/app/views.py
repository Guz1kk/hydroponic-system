from app.models import System
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from app.serializers import SystemsSerializer, MeasurementSerializer
from django.shortcuts import get_object_or_404


class SystemsView(APIView):
    """ All systems view """
    
    def get(self, request) -> JsonResponse:
        """ All system get """
        #user = self.request.user
        systems = System.objects.all()
        response = SystemsSerializer(systems, many=True)
        return JsonResponse(response.data, safe=False)

    def post(self, request) -> HttpResponse:
        from django.contrib.auth.models import User
        data = self.request.data
        #user = self.request.user
        user = User.objects.get(username='admin')
        system = System(name=data['name'], user = user)
        system.save()
        return HttpResponse(status=201)
    
    

class SingleSystemView(APIView):
    """ Single system view """
    
    def get(self, request, systemID:int) -> JsonResponse:
        """Single system indo

        Args:
            systemID (int): system id

        Returns:
            HttpResponse: HTTP 404 if object not found
            JsonResponse: system info JSON
        """
        system = get_object_or_404(System, pk=systemID)
        response = SystemsSerializer(system, many=False)
        return JsonResponse(response.data, safe=False)
    
    
    def delete(self, request, systemID:int) -> HttpResponse:
        """_summary_

        Args:
            systemID (int): system id

        Returns:
            HttpResponse: HTTP 204 - succesfull delete
                          HTTP 404 - object not found
        """
        system = get_object_or_404(System, pk=systemID)
        system.delete()
        return HttpResponse(status=204)
    

class MeasurementView(APIView):
    """ Measurement view """
    
    def post(self, request) -> HttpResponse:
        serializer = MeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=201)
        return HttpResponse(status=400)