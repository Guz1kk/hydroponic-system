from django.db import models
from django.contrib.auth.models import User


class System(models.Model):
    """ System model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    
    class Meta:
        unique_together = ['user', 'name']
        
    def __str__(self) -> str:
        return self.name
    
class Measurement(models.Model):
    """ Measurements model """
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    sensor = models.CharField(max_length=30)
    ph = models.DecimalField(max_digits=3, decimal_places=1)
    water_temperature = models.DecimalField(max_digits=4, decimal_places=1)
    tds = models.DecimalField(max_digits=5, decimal_places=2)
    time = models.DateTimeField()
    
    def __str__(self):
        return f'{self.sensor} - {self.time}'