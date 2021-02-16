from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import FileSerializer
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import re, json, requests
from oauth2client import file
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer
from rest_framework import permissions
import os
from django.http import HttpResponse
from datetime import date

# def post(self, request, *args, **kwargs):      
#       file_serializer = FileSerializer(data=request.data)
#       if file_serializer.is_valid():
#           file_serializer.save()
#           return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#       else:
#           return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)    
    destination = '/Documents'
    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)
        # To create a new folder
        # folder_name = input("Name the Folder : ")
        
        SCOPES = 'https://www.googleapis.com/auth/drive.metadata'
        with open('/home/thasleem/2021-projects/backend/uploadapp/token.json', 'r') as f:
            my_json_obj = json.load(f)
            print(my_json_obj, type(my_json_obj))
            print(file_serializer,'file')
            if file_serializer.is_valid():
                file_serializer.save()
                uploaded_file = request.FILES['file']
                print(uploaded_file, 'uploaded_file')
                print(uploaded_file.name,'uploaded_file',type(uploaded_file.name))
                store = file.Storage('/home/thasleem/2021-projects/backend/media/uploadapp/token.json')
                creds = store.get()
                folder_name = '19_02_2021'
                folder = drive.CreateFile({'title' : folder_name, 'mimeType' : 'application/vnd.google-apps.folder'})
                folder.Upload()
                drive = GoogleDrive(gauth)
                folder_list = drive.ListFile({'q': "trashed=false"}).GetList()
                f = drive.CreateFile({"title":uploaded_file.name,"parents": [{"kind": "drive#fileLink", "id": folder['id']}]})
                # Make sure to add the path to the file to upload below.
                path = r"/home/thasleem/2021-projects/backend/media"
                f.SetContentFile(os.path.join(path, uploaded_file.name))
                f.Upload()
                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    response = requests.get('http://freegeoip.net/json/')
    geodata = response.json()
    return render(request, 'uploadapp/home.html', {
        'ip': geodata['ip'],
        'country': geodata['country_name']
    })

# def http_response(request):
#     return HttpResponse("This is a simple response !")