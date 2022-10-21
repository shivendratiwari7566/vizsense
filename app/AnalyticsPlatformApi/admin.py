from django.contrib import admin
#from  AnalyticsPlatformApi.models import Functions
from  AnalyticsPlatformApi.models import processed_video, Functions,Sources,sub_sources,Cameras,Groups,Jobs,Tasks,Operations,Model_labels,Models,Function_parameters,log,streaming_url, Function_lto
# Register your models here.
#myModels=[Functions]
#myModels=[models.Functions,models.Sources,models.sub_sources,models.Cameras,models.Groups,models.Jobs,models.Tasks,models.Operations,models.Models,models.Model_labels,models.Function_parameters,models.log,models.streaming_url]
admin.site.register(Functions)
admin.site.register(Sources)
admin.site.register(sub_sources)
admin.site.register(Cameras)
admin.site.register(Groups)
admin.site.register(Jobs)
admin.site.register(Tasks)
admin.site.register(Operations)
admin.site.register(Model_labels)
admin.site.register(Models)
admin.site.register(Function_parameters)
admin.site.register(log)
admin.site.register(streaming_url)
admin.site.register(Function_lto)
admin.site.register(processed_video)



