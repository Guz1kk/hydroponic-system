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