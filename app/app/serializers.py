from rest_framework import serializers
from app.models import System


class SystemsSerializer(serializers.ModelSerializer):
    """ All systems serializer """
    class Meta:
        model = System
        fields = '__all__'