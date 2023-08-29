from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserMessageSerializer
from .models import UserMessage
from user.models import User
from django.db.models import Avg

class UserIsStressAPI(GenericAPIView):
    def get(Self,request):
        try: 
            user = request.user
            user_mod_avg = UserMessage.objects.filter(user=user).aggregate(Avg('is_stressed'))
            print(user.username)
            return Response({
                'user':user.username,
                'stress':user_mod_avg['is_stressed__avg']
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message':'exception',
                'error': str(e)
            },status=status.HTTP_501_NOT_IMPLEMENTED)

class UserMessageAPI(ListCreateAPIView):
    serializer_class = UserMessageSerializer
    queryset = UserMessage.objects.all()
    
    def get(self, request):
        try:
            user_messages = self.get_queryset()
            serializer = UserMessageSerializer(user_messages, many=True)
            return Response({
                'message': 'success',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'An exception occurred',
                'exception': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self,request):
        
        try:
            serializer = UserMessageSerializer(data=request.data,context={'user': request.user})
            print(request.data['message'])
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message':'success',
                    "data":serializer.data,
                    },status=status.HTTP_200_OK)
            else:
                return Response({
                    'message':'serializer not valid',
                    'error': serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error':'An exception occured',
                'exception':str(e),
            }
            ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

        
            


