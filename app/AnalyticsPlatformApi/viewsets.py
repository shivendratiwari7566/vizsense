from rest_framework import viewsets
from . import models
from . import serializers

#test_one
class EmployeeViewset(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

class FunctionsViewset(viewsets.ModelViewSet):
    queryset = models.Functions.objects.all()
    serializer_class = serializers.FunctionsSerializer

class CamerasViewset(viewsets.ModelViewSet):
    queryset = models.Cameras.objects.all()
    serializer_class = serializers.CamerasSerializer

class SourcesViewset(viewsets.ModelViewSet):
    queryset = models.Sources.objects.all()
    serializer_class = serializers.SourcesSerializer

class GroupsViewset(viewsets.ModelViewSet):
    queryset = models.Groups.objects.all()
    serializer_class = serializers.GroupsSerializer

class UsersViewset(viewsets.ModelViewSet):
    queryset = models.Users.objects.all()
    serializer_class = serializers.UsersSerializer

class ModelsViewset(viewsets.ModelViewSet):
    queryset = models.Models.objects.all()
    serializer_class = serializers.ModelsSerializer

class JobsViewset(viewsets.ModelViewSet):
    queryset = models.Jobs.objects.all()
    print("-------------------------->",queryset)
    serializer_class = serializers.JobSerializer

