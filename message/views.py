from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .serializers import UserMessageSerializer,UserMessageCSVSerializer
from .models import UserMessage
from user.models import User
from django.db.models import Avg
from datetime import datetime
from decouple import config
import csv
import os
import cloudinary
import cloudinary.uploader

cloudinary.config( 
  cloud_name = config('CLOUD_NAME'), 
  api_key = config('API_KEY'), 
  api_secret = config('API_SECRET') 
)

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

class UserMessageCSVAPI(GenericAPIView):
    # permission_classes = [IsAdminUser]
    def __init__(self):
        # Create the CSV directory if it doesn't exist
        csv_dir = 'project/csv_files'
        os.makedirs(csv_dir, exist_ok=True)
        super().__init__()
        
    def get(self,request):
        try:
            for i in User.objects.all().values():
                if UserMessage.objects.filter(user_id=i['id']):  
                    print(i['username'])
                    print(UserMessage.objects.filter(user=i['id']).aggregate(Avg('is_stressed'))['is_stressed__avg'])
            filename = f"all_user.csv"
            file_path = os.path.join("project/csv_files", filename).replace("\\", "/")
            file_exists = os.path.isfile(file_path)
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Create and write data to the CSV file
            with open(file_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                if not file_exists:
                    writer.writerow(["Timestamp","user",'average_percentage'])
                for i in User.objects.all().values():
                    if UserMessage.objects.filter(user_id=i['id']):
                        avg = UserMessage.objects.filter(user=i['id']).aggregate(Avg('is_stressed'))['is_stressed__avg']
                        writer.writerow([current_timestamp,i['username'],avg])

            upload_result = cloudinary.uploader.upload(
                file_path, 
                resource_type="raw", 
                public_id=file_path, 
                overwrite=True  
            )
            csv_url = upload_result['secure_url']
            return Response({'message':'succuess','url':csv_url})
        except Exception as e:
            return Response({"message":'exception',"exception":str(e)}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
class MessageCSVAPI(GenericAPIView):
    permission_classes = [IsAdminUser]
    
    def __init__(self):
        # Create the CSV directory if it doesn't exist
        csv_dir = 'project/csv_files'
        os.makedirs(csv_dir, exist_ok=True)
        super().__init__()
        
    
    def get(self, request):
        try:
            queryset = UserMessage.objects.all()
            serializer = UserMessageCSVSerializer(queryset, many=True)
            data = serializer.data
            filename = f"data_stress.csv"
            file_path = os.path.join("project/csv_files", filename).replace("\\", "/")
            file_exists = os.path.isfile(file_path)
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Create and write data to the CSV file
            with open(file_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                if not file_exists:
                    writer.writerow(["Timestamp","prompt","response"])  # Write header only if the file is newly created
                for row in data:
                    writer.writerow([current_timestamp,row['message'],row['is_stressed']])

            upload_result = cloudinary.uploader.upload(
                file_path, 
                resource_type="raw", 
                public_id=file_path,  # Set the custom filename
                overwrite=True  # Overwrite if a file with the same name exists
            )
            csv_url = upload_result['secure_url']
            return Response({'csv_url': csv_url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message":'exception',"exception":str(e)}, status=status.HTTP_501_NOT_IMPLEMENTED)
