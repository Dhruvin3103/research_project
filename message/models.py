from django.db import models
from user.models import User
# Create your models here.

class UserMessage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    is_stressed = models.IntegerField(default=0)
    
    
    def __str__(self) -> str:
        return  str(self.message)
    