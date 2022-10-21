from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import pandas as pd
from .models import Cameras, ModelsDevelop
from .serializers import *

class DeviceViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Cameras.objects.filter(status='active')
        serializer = CamerasSerializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request):
        serializer = CamerasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":200,"message":"success"})

    def update(self, request, pk=None):
        instance = Cameras.objects.get(id=pk)
        serializer = CamerasSerializer(data=request.data,instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":200,"message":"success"})

    @action(detail=True, url_path='bulk', methods=['OPTIONS', 'POST'])
    def bulk_create(self,request,pk=None):
        serializer = CamersBulkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_data = request.FILES.get('devices')
        df = pd.read_csv(file_data)
        bulk_create_objs = []
        for _, item in df.iterrows():
            obj = Cameras(
                camera_name = item['name'],
                url = item['link'],
                latitude = item['latitude'],
                longitude = item['longitute']
            )
            bulk_create_objs.append(obj)
        Cameras.objects.bulk_create(bulk_create_objs)
        return Response({"status":200,"message":"success"})

    @action(detail=True, url_path='delete', methods=['OPTIONS', 'POST'])
    def bulk_delete(self,request,pk=None):
        ids = request.data.get("ids") # '[1,2,3]'
        Cameras.objects.filter(id__in=eval(ids)).update(status='inactive')
        return Response({"status":200,"message":"delete success"})

        
        
class ModelsViewSet(viewsets.ViewSet):

    def list(self,request):
        queryset = ModelsDevelop.objects.all()
        serializer = ModelDevSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ModelDevSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":200,"message":"success"})

    def update(self, request, pk=None):
        instance = ModelsDevelop.objects.get(id=pk)
        serializer = ModelDevSerializer(data=request.data,instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":200,"message":"success"})


# class CycleTrainingViewSet(viewsets.ViewSet):

#     def list(self,request):
#         queryset = CycleTraining.objects.all()
#         serializer = CycleTrainingSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = CycleTrainingSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"status":200,"message":"success"})

#     def update(self, request, pk=None):
#         instance = CycleTraining.objects.get(id=pk)
#         serializer = CycleTrainingSerializer(data=request.data,instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"status":200,"message":"success"})