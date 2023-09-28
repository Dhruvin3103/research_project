from django.db import models
from user.models import User
# Create your models here.

class UserMessage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    time = models.DateTimeField(auto_now=True)
    is_stressed = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return  str(self.message)
    
class FormScore(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    form = models.CharField(max_length=200,null=True,blank=True)
    time = models.DateTimeField(auto_now=True)
    score = models.PositiveBigIntegerField()
    
    def __str__(self) -> str:
        return str(self.user)+"  "+str(self.score)
    