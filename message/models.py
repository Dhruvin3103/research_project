from django.db import models
from user.models import User
# Create your models here.

class UserMessage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    is_stressed = models.BooleanField()
    
    
    def __str__(self) -> str:
        return  self.id +str(self.user) + str(self.is_stressed())
    