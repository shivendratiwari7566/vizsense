from rest_framework import serializers
from .models import *

# #test_one
# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = '__all__'

# # #1
# class FunctionsSerializer(serializers.ModelSerializer):
#     # specify model and fields
#     class Meta:
#         model = Functions
#         fields = '__all__'

# 2       
# class CamerasSerializer(serializers.ModelSerializer):
#     # specify model and fields
#     class Meta:
#         model = Cameras
#         fields = '__all__'

# #3
# class SourcesSerializer(serializers.ModelSerializer):
#     # specify model and fields
#     class Meta:
#         model = Sources
#         fields = '__all__'

# #4        
# class GroupsSerializer(serializers.ModelSerializer):
#     # specify model and fields
#     class Meta:
#         model = Groups
#         fields = '__all__'

# #5
# class UsersSerializer(serializers.ModelSerializer):
#     # specify model and fields
#     class Meta:
#         model = Users
#         fields = '__all__'

# #6        
# class ModelsSerializer(serializers.ModelSerializer):
#     # specify model and fields
#     class Meta:
#         model = Models
#         fields = '__all__'

# #7
# #create jobs
# class JobSerializer(serializers.ModelSerializer):
#     # specify model and fields
#     class Meta:
#         model = Jobs
#         fields = '__all__'



class CamerasSerializer(serializers.ModelSerializer):
    url = serializers.CharField(required=True)
    class Meta:
        model = Cameras
        fields = ['camera_name','url','location','latitude','longitude','id']

class CamersBulkSerializer(serializers.Serializer):
    devices = serializers.FileField(required=True)
    
class ModelDevSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelsDevelop
        fields = '__all__'

# class CycleTrainingSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = CycleTraining
#         fields = '__all__'