from django.shortcuts import render
from app.models import System
from rest_framework.views import APIView
from django.http import JsonResponse
from app.serializers import SystemsSerializer


class SystemsView(APIView):
    """ All systems view """
    
    def get(self, request):
        """ All system get """
        #user = self.request.user
        systems = System.objects.all()
        response = SystemsSerializer(systems, many=True)
        return JsonResponse(response.data, safe=False)