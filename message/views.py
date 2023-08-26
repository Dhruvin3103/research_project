from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserMessageSerializer
from .models import UserMessage


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
            print(request.user)
            
            serializer = UserMessageSerializer(data=request.data,context={'user': request.user})
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
            

        
            


