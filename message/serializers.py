from rest_framework import serializers

from .models import UserMessage

class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = ['message']
        
    def create(self, validated_data):
        
        user = self.context.get('user')
        print(validated_data,user)
        # user = request.user
        # print(kwargs)
        validated_data['user'] = user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        print(instance.user)
        data = super().to_representation(instance)
        print(data)
        data['user'] = instance.user.username
        data['is_stressed'] = instance.is_stressed
        print(data)
        return data