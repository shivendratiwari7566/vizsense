from django.db import models
import datetime
from django.contrib.postgres.fields import ArrayField

#1
class Functions(models.Model):
    function_id=models.BigIntegerField(primary_key=True)
    function_name = models.CharField(max_length=200)
    function_type = models.CharField(max_length=200)    
    class Meta:
        db_table  = "Functions"

#2
class Sources(models.Model):
    source_id =models.BigIntegerField(primary_key=True)
    source_name = models.CharField(max_length=200)
    source_type = models.CharField(max_length=200)
    cameras = models.TextField(blank=True, null=True)
    sub_sources = models.TextField(blank=True, null=True)
    class Meta:
        db_table = "Sources"

#3
class sub_sources(models.Model):
    sub_source_id = models.BigIntegerField(primary_key=True)    
    sub_source_name = models.CharField(max_length=200)
    folder_path = models.TextField(blank=True, null=True)
    class Meta:
        db_table = "sub_sources"

STATUS = (('active',"ACTIVE"),('inactive','INACTIVE'))
class Cameras(models.Model):
    # camera_id = models.BigIntegerField(primary_key=True)
    status = models.CharField(choices=STATUS,max_length=10,default='active')
    camera_name = models.CharField(max_length=200)
    url = models.CharField(blank=True,max_length=1200)
    # url = models.URLField(blank=True)
    location = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    #                                                                        username =  models.CharField(max_length=200)
    #password =  models.CharField(max_length=200)

    # class Meta:
    #     db_table = "Cameras"

    def ___str__(self):
        return self.camera_name
#4
class Groups(models.Model):
    groups_id=models.BigIntegerField(primary_key=True)
    group_name = models.CharField(max_length=200)
    class Meta:
        db_table = "Groups"

#5
class Jobs(models.Model):     
    job_id=models.BigIntegerField(primary_key=True)
    job_name = models.CharField(max_length=200)
    recurrence = models.CharField(max_length=200)
    from_date = models.DateField('from date')
    to_date = models.DateField('to date',blank=True, null=True) 
    start_time = models.TimeField()
    sme_alert=models.BooleanField(blank=True, null=True)
    email_alert=models.BooleanField(blank=True, null=True)   
    function = models.ForeignKey(Functions,on_delete=models.CASCADE)
    source = models.ForeignKey(Sources, on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,default='INQUEUE')
    class Meta:
        db_table  = "Jobs"

#6
class Tasks(models.Model):
    #tasks_id=models.AutoField(primary_key=True)
    tasks_id = models.BigIntegerField(primary_key=True)
    task_name = models.CharField(max_length=200)
    class Meta:
        db_table  = "Tasks"

#7
class Operations(models.Model):
    #operation_id=models.AutoField(primary_key=True, default=0)
    operation_id = models.BigIntegerField(primary_key=True)
    operation_name = models.CharField(max_length=200)
    class Meta:
        db_table  = "Operations"

# 8
class Models(models.Model):
    #model_id=models.AutoField(primary_key=True, default=0)
    model_id = models.BigIntegerField(primary_key=True)
    model_name = models.CharField(max_length=200)
    architecture = models.CharField(max_length=200)
    label_file_path = models.TextField(blank=True, null=True) 
    model_file_path = models.TextField(blank=True, null=True)
    model_specname= models.TextField(blank=True, null=True, default="obj_detection") 
    model_signature = models.TextField(blank=True, null=True, default="serving_default") 
    comments = models.TextField(blank=True, null=True, default="comments")
    class Meta:
        db_table  = "Models"

#9
class Model_labels(models.Model):
    #label_id=models.AutoField(primary_key=True, default=0)
    label_id = models.BigIntegerField(primary_key=True)
    model_label_id= models.BigIntegerField(default=1)     
    model = models.ForeignKey(Models, on_delete=models.CASCADE)
    label_name = models.CharField(max_length=200)

    class Meta:
        db_table  = "Model_labels"

# #10
class Function_lto(models.Model):
    lto_id=models.BigIntegerField(primary_key=True)
    function = models.ForeignKey(Functions,on_delete=models.CASCADE)
    label = models.ForeignKey(Model_labels,on_delete=models.CASCADE)
    operation = models.ForeignKey(Operations,on_delete=models.CASCADE)
    # task_id= models.ForeignKey(Tasks,on_delete=models.CASCADE)  
    class Meta:
        db_table  = "Function_lto"

# #10
class Function_parameters(models.Model):
    param_id =models.BigIntegerField(primary_key=True)
    function = models.ForeignKey(Functions,on_delete=models.CASCADE)
    param_name = models.CharField(max_length=200)
    param_type = models.CharField(max_length=20)      
    class Meta:
        db_table  = "Function_parameters"

class log(models.Model):
    detectionid = models.IntegerField(primary_key=True)
    functiontype = models.CharField(max_length=200)
    objectid = models.IntegerField()
    filename=models.CharField(max_length=200)
    framecount=models.IntegerField()
    totalframes = models.IntegerField()
    classid = models.BigIntegerField()
    classname = models.CharField(max_length=200)
    coordinates=models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField('timestamp')
    jobid = models.BigIntegerField(default=1) #models.ForeignKey(Jobs,on_delete=models.CASCADE) 
    sourceid = models.BigIntegerField(default=1) #models.ForeignKey(Sources,on_delete=models.CASCADE)
    sub_sourceid = models.BigIntegerField(default=1) #models.ForeignKey(sub_sources,on_delete=models.CASCADE)
    sub_sourcename=models.CharField(max_length=200, default="vid")
    retscore=models.IntegerField(default=50)
    model_label_id = models.IntegerField(default=1)
    class Meta:
        db_table  = "log"


class streaming_url(models.Model):
    jobid = models.BigIntegerField(primary_key=True)
    sub_source_id = models.BigIntegerField()
    url = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50,default='Running')
    class Meta:
        db_table  = "streaming_url"


class processed_video(models.Model):

    processed_video_id = models.IntegerField(primary_key=True)
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE)
    sub_source=models.CharField(max_length=200)
    #camera_id = models.CharField(max_length=200)
    video_file_name=models.CharField(max_length=200)
    processed_date=models.TextField(blank=True, null=True)
    path=models.TextField(blank=True, null=True)
    source_type =models.CharField(max_length=200)
    class Meta:
        db_table = "processed_video"



class ModelsDevelop(models.Model):
    name = models.CharField(max_length=1200,verbose_name="Model Name")
    description = models.TextField(verbose_name="Model Description")

    def __str__(self) -> str:
        return super().__str__(self.name)

