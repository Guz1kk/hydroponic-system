from rest_framework import serializers
from app.models import System, Measurement


class SystemsSerializer(serializers.ModelSerializer):
    """ All systems serializer """
    class Meta:
        model = System
        fields = '__all__'
        
    
class MeasurementSerializer(serializers.ModelSerializer):
    """ Measurement serializer """
    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'ph', 'water_temperature', 'tds', 'time']