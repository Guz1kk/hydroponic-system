from rest_framework import serializers
from app.models import System, Measurement


class SystemsSerializer(serializers.ModelSerializer):
    """ All systems serializer """
    class Meta:
        model = System
        fields = ['id', 'user', 'name']
        extra_kwargs = {
            'user': {'read_only': True}
        }
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
        
    
class MeasurementSerializer(serializers.ModelSerializer):
    """ Measurement serializer """
    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'ph', 'water_temperature', 'tds', 'time']
        

class SingleSystemSerializer(serializers.ModelSerializer):
    measurements = serializers.SerializerMethodField()

    class Meta:
        model = System
        fields = '__all__'

    def get_measurements(self, obj):
        latest_measurements = obj.measurements.order_by('-time')[:10]
        return MeasurementSerializer(latest_measurements, many=True).data