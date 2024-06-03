from rest_framework import serializers
from app.models import System, Measurement


class SystemsSerializer(serializers.ModelSerializer):
    """ All systems serializer """
    class Meta:
        model = System
        fields = ['id', 'user', 'name', 'info']
        extra_kwargs = {
            'user': {'read_only': True}
        }
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.info = validated_data.get('info', instance.info)
        instance.save()
        return instance
        
    
class MeasurementSerializer(serializers.ModelSerializer):
    """ Measurement serializer """
    system = SystemsSerializer()
    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'ph', 'water_temperature', 'tds', 'time','system']
        

class SingleSystemSerializer(serializers.ModelSerializer):
    measurements = serializers.SerializerMethodField()

    class Meta:
        model = System
        fields = '__all__'

    def get_measurements(self, obj):
        latest_measurements = obj.measurement_set.order_by('-time')[:10]
        return MeasurementSerializer(latest_measurements, many=True).data