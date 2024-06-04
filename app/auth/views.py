from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse


class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["access_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return HttpResponse(status=205)
        except Exception as e:
            return HttpResponse(status=400)