from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from AnalyticsPlatformApi import models
from AnalyticsPlatformApi import views
from django.conf import settings
from django.core import serializers
from pathlib import Path
from datetime import datetime, timedelta
import json
import os
import time
from rest_framework.decorators import api_view
import psycopg2
from collections import Counter
#from AnalyticsPlatformApi.update_json import update_json
#from AnalyticsPlatformApi.update_json import eta_days


import ast
import pathlib
from django.core.files.storage import FileSystemStorage
import datetime
import os
import sys
import shutil

# from log_database import database_function

try:
    # from Worker.worker import job_app
    from Inference_copy.worker import job_app
    from log_database import database_function
except:
    # from AnalyticsPlatformApi.Worker.worker import job_app
    #from AnalyticsPlatformApi.Inference_copy.worker import job_app
    from .log_database import database_function

#from celery.execute import send_task

current_date = datetime.datetime.now()


# views test funtions
@api_view(['GET', 'POST', ])
def test_views(request):
    if request.method == 'GET':
        return HttpResponse("Get method")
    elif request.method == 'POST':
        return HttpResponse("Post method")


# Create your views here.
def home_view(request):
    return render(request, "index.html")


# Funtions
@api_view(['GET', 'POST', ])
def function_create(request):
    try:
        # 
        request_json = json.loads(request.body)
        event = request_json["data"]
        current_date = datetime.datetime.now()
        Id_val = current_date.strftime("%Y%m%d%H%M%S")
        Functions_create = models.Functions(
            function_id=Id_val,
            function_name=event["function_name"],
            function_type=event["function_type"])
        Functions_create.save()
        # create labels_tasks_operation           
        labels_tasks_operation = event["labels_tasks_operation"]
        labels_tasks_operation_res = function_labels_tasks_operation_create(Id_val, labels_tasks_operation)
        if labels_tasks_operation_res["status"] == "success":
            # create parameters
            parameters = event["parameters"]
            print(parameters)
            parameters_res = function_parameters_create(Id_val, parameters)
            if parameters_res["status"] == "success":
                event["function_id"] = Id_val
                res = {"status": "success", "message": "Function created successfully", "data": event}
                return JsonResponse(res)
            else:
                return JsonResponse(parameters_res)
        else:
            return JsonResponse(labels_tasks_operation_res)
    except Exception as e:
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


# Funtions_labels_tasks_operation create
def function_labels_tasks_operation_create(function_id, eventdata):
    try:
        for event in eventdata:
            current_date = datetime.datetime.now()
            Id_val = current_date.strftime("%Y%m%d%H%M%S%f")
            print("-----function_labels_tasks_operation----", Id_val, Id_val[:-1])
            Function_lto_create = models.Function_lto(
                lto_id=Id_val[:-1],
                function_id=function_id,
                label_id=event["label_id"],
                operation_id=event["operation_id"])
            Function_lto_create.save()
        res = {"status": "success", "message": "function_labels_tasks_operation created successfully"}
        return (res)
    except Exception as e:
        res = {"status": "failed", "message": "function_labels_tasks_operation:" + str(e)}
        return (res)


def function_labels_tasks_operation_getDetails(event):
    try:
        functions_res = json.loads(
            serializers.serialize("json", models.Function_lto.objects.filter(function_id=event["function_id"])))
        res = []
        for i in functions_res:
            fields = i["fields"]
            label_name = json.loads(
                serializers.serialize("json", models.Model_labels.objects.filter(label_id=fields["label"])))
            operation_name = json.loads(
                serializers.serialize("json", models.Operations.objects.filter(operation_id=fields["operation"])))
            fields['lto_id'] = i["pk"]
            fields['label_id'] = fields['label']
            del fields['label']
            fields["label_name"] = label_name[0]["fields"]["label_name"]
            fields['operation_id'] = fields['operation']
            del fields['operation']
            fields["operation_name"] = operation_name[0]["fields"]["operation_name"]
            res.append(fields)
        res = {"status": "success", "message": "Functions_lto get is success", "data": (res)}
        print(res)
        return (res)
    except Exception as e:
        res = {"status": "failed", "message": "function_labels_tasks_operation_getDetails:" + str(e)}
        return (res)


def function_labels_tasks_operation_update(function_id, eventdata):
    try:
        jobs_res = models.Function_lto.objects.filter(function_id=function_id).delete()
        print("-----------------____________------------")
        print(jobs_res)
        print("------------------______________------------")
        for event in eventdata:
            current_date = datetime.datetime.now()
            Id_val = current_date.strftime("%Y%m%d%H%M%S%f")
            print("-----function_labels_tasks_operation----", Id_val, Id_val[:-1])

            Function_lto_update = models.Function_lto(
                lto_id=Id_val[:-1],
                function_id=function_id,
                label_id=event["label_id"],
                operation_id=event["operation_id"])
            Function_lto_update.save()
        res = {"status": "success", "message": "function_labels_tasks_operation_update update successfully"}
        return (res)
    except Exception as e:
        res = {"status": "failed", "message": "function_labels_tasks_operation_update:" + str(e)}
        return (res)


# Funtions_parameters
def function_parameters_create(function_id, eventdata):
    try:
        for event in eventdata:
            current_date = datetime.datetime.now()
            Id_val = current_date.strftime("%Y%m%d%H%M%S%f")
            print("-----function_parameters----", Id_val, Id_val[:-1])
            Functions_create = models.Function_parameters(
                param_id=Id_val[:-1],
                function_id=function_id,
                param_name=event["param_name"],
                param_type=event["param_type"]
            )
            Functions_create.save()
        res = {"status": "success", "message": "function_parameters created successfully"}
        return (res)
    except Exception as e:
        res = {"status": "failed", "message": "function_parameters:" + str(e)}
        return (res)


def function_parameters_getDetails(event):
    try:
        functions_res = json.loads(
            serializers.serialize("json", models.Function_parameters.objects.filter(function_id=event["function_id"])))
        res = []
        for i in functions_res:
            fields = i["fields"]
            fields['param_id'] = i["pk"]
            res.append(fields)
        res = {"status": "success", "message": "function_parameters_getDetails get is success", "data": (res)}
        print(res)
        return (res)
    except Exception as e:
        res = {"status": "failed", "message": "function_parameters_getDetails:" + str(e)}
        return (res)


@api_view(['GET', 'POST', ])
def function_getparameters(request):
    try:
        event = json.loads(request.body)
        functions_res = json.loads(
            serializers.serialize("json", models.Function_parameters.objects.filter(function_id=event["function_id"])))
        res = []
        for i in functions_res:
            fields = i["fields"]
            fields['param_id'] = i["pk"]
            fields['function_id'] = fields['function']
            del fields['function']
            res.append(fields)
        res = {"status": "success", "message": "function_parameters_getDetails get is success", "data": (res)}
        return JsonResponse(res)
    except Exception as e:
        res = {"status": "failed", "message": "function_getparameters:" + str(e)}
        return JsonResponse(res)


def function_parameters_update(function_id, eventdata):
    try:
        for event in eventdata:
            Functions_update = models.Function_parameters(
                param_id=event["param_id"],
                function_id=function_id,
                param_name=event["param_name"],
                param_type=event["param_type"]
            )
            Functions_update.save()
        res = {"status": "success", "message": "function_parameters update successfully"}
        return (res)
    except Exception as e:
        res = {"status": "failed", "message": "function_parameters update:" + str(e)}
        return (res)


@api_view(['GET', 'POST', ])
def functions_get(request):
    try:
        functions_res = json.loads(serializers.serialize("json", models.Functions.objects.all()))
        print(functions_res)
        res = []
        for i in functions_res:
            fields = i["fields"]
            fields['function_id'] = i["pk"]
            res.append(fields)
        res = {
            "status": "success",
            "message": "Functions get is success",
            "data": (res)
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def functions_getDetails(request):
    try:
        event = json.loads(request.body)
        functions_res = json.loads(
            serializers.serialize("json", models.Functions.objects.filter(function_id=event["function_id"])))
        print(functions_res)
        if len(functions_res) != 0:
            res = []
            for i in functions_res:
                fields = i["fields"]
                fields['function_id'] = i["pk"]
                res.append(fields)
            function_lto_res = function_labels_tasks_operation_getDetails(event)
            if function_lto_res["status"] == "success":
                fields["labels_tasks_operation"] = function_lto_res["data"]
                Function_parameters_res = function_parameters_getDetails(event)
                if Function_parameters_res["status"] == "success":
                    fields["parameters"] = Function_parameters_res["data"]
                    res.append(fields)
                    res = {"status": "success", "message": "function not found", "data": res}
                    return JsonResponse(res)
                else:
                    return JsonResponse(Function_parameters_res)
            else:
                return JsonResponse(function_lto_res)
        else:
            res = {"status": "success", "message": "function not found", "data": []}
            return JsonResponse(res)


    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def functions_delete(request):
    # Read a specific entry:
    event = json.loads(request.body)
    try:
        jobs_res = models.Functions.objects.filter(function_id=event["function_id"]).delete()
        res = {
            "status": "success",
            "message": "Delete Functions is success"
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def function_update(request):
    try:
        # 
        request_json = json.loads(request.body)
        event = request_json["data"]
        Functions_update = models.Functions(
            function_id=event["function_id"],
            function_name=event["function_name"],
            function_type=event["function_type"])
        Functions_update.save()
        # update labels_tasks_operation           
        labels_tasks_operation = event["labels_tasks_operation"]
        print("==============================================")
        print(labels_tasks_operation)
        print("==========================================================")
        labels_tasks_operation_res = function_labels_tasks_operation_update(event["function_id"],
                                                                            labels_tasks_operation)
        if labels_tasks_operation_res["status"] == "success":
            # update parameters
            parameters = event["parameters"]
            parameters_res = function_parameters_update(event["function_id"], parameters)
            if parameters_res["status"] == "success":
                res = {"status": "success", "message": "Functions Updated successfully"}
                return JsonResponse(res)
            else:
                return JsonResponse(parameters_res)
        else:
            return JsonResponse(labels_tasks_operation_res)
    except Exception as e:
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


# Sources
@api_view(['GET', 'POST', ])
def sources_create(request):
    try:
        request_json = json.loads(request.body)
        event = request_json["data"]
        current_date = datetime.datetime.now()
        Id_val = current_date.strftime("%Y%m%d%H%M%S")
        if event["source_type"] == "Live":
            Sources_create = models.Sources(
                source_id=Id_val,
                source_name=event["source_name"],
                source_type=event["source_type"],
                cameras=json.dumps(event["cameras"]),
                sub_sources=event["sub_sources"]
            )
            Sources_create.save()
            event['source_id'] = Id_val
            res = {"status": "success", "message": "Sources created successfully", "data": event}
            return JsonResponse(res)
        elif event["source_type"] == "Video":  # and event["source_type"]=="Image":
            sub_sources = event["sub_sources"]
            sub_sources_res = sub_sources_create(sub_sources)
            if sub_sources_res["status"] == "success":
                Sources_create = models.Sources(
                    source_id=Id_val,
                    source_name=event["source_name"],
                    source_type=event["source_type"],
                    cameras=event["cameras"],
                    sub_sources=json.dumps(sub_sources_res["sub_sources_ids"])
                )
                Sources_create.save()
                event['source_id'] = Id_val
                event["sub_sources"] = sub_sources_res["data"]
                res = {"status": "success", "message": "Sources created successfully", "data": event}
                return JsonResponse(res)
            else:
                res = {"status": "success", "message": "Sources created successfully", }
                return JsonResponse(res)
        else:
            res = {"status": "failed", "message": sub_sources_res["message"]}
            return JsonResponse(res)
    except Exception as e:
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


def sub_sources_create(eventdata):
    try:
        final_eventdata = []
        # print("eneventdataaaaa______", eventdata)
        sub_sources_ids = []
        for event in eventdata:
            current_date = datetime.datetime.now()
            Id_val = current_date.strftime("%Y%m%d%H%M%S")
            Id_val = str(int(Id_val) + 1)
            sub_sources_create = models.sub_sources(
                sub_source_id=Id_val,
                sub_source_name=event["sub_source_name"],
                folder_path=event["folder_path"])
            sub_sources_create.save()
            event['sub_source_id'] = Id_val
            final_eventdata.append(event)
            # sub_sources_ids.append(Id_val)

            sub_sources_ids.append(Id_val)
            time.sleep(1)
        res = {"status": "success", "message": "sub_sources created successfully", "data": event,
               "sub_sources_ids": sub_sources_ids}
        return (res)
    except Exception as e:
        res = {"status": "failed", "message": str(e)}
        return (res)


@api_view(['GET', 'POST', ])
def sources_get(request):
    try:
        sources_res = json.loads(serializers.serialize("json", models.Sources.objects.all()))
        res = []
        for i in sources_res:
            print("--------", i)
            fields = i["fields"]
            fields['source_id'] = i["pk"]
            if fields['source_type'] == 'Live':
                fields['cameras'] = json.loads(fields["cameras"])
            elif fields['source_type'] == 'Video':  # and fields['source_type']=='Image':
                fields['sub_sources'] = json.loads(fields["sub_sources"])
            res.append(fields)
        res = {
            "status": "success",
            "message": "Sources get is success",
            "data": (res)
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def sources_delete(request):
    # Read a specific entry:
    event = json.loads(request.body)
    try:
        jobs_res = models.Sources.objects.filter(source_id=event["source_id"]).delete()
        res = {
            "status": "success",
            "message": "Delete Sources is success"
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def sources_details(request):
    try:
        event = json.loads(request.body)
        sources_res = json.loads(
            serializers.serialize("json", models.Sources.objects.filter(source_id=event["source_id"])))
        res = []
        for i in sources_res:
            if len(i) != 0:
                sources_data = i["fields"]
                sources_data['source_id'] = i["pk"]
                if sources_data["source_type"] == "Live":
                    cameras_list = json.loads(sources_data["cameras"])
                    cam_data = []
                    if len(cameras_list) != 0:
                        for cam in cameras_list:
                            sources_res = json.loads(
                                serializers.serialize("json", models.Cameras.objects.filter(id=cam)))
                            if len(sources_res) != 0:
                                for i in sources_res:
                                    fields = i["fields"]
                                    fields['camera_id'] = i["pk"]
                                    cam_data.append(fields)
                    sources_data["cameras"] = cam_data
                    res.append(sources_data)
                    res = {"status": "success", "message": "sources_details get is success", "data": (res)}
                    return JsonResponse(res)
                elif sources_data["source_type"] == "Video":  # and sources_res["source_type"]=="Image":
                    sub_sources_list = json.loads(sources_data["sub_sources"])
                    sub_sources_data = []
                    if len(sub_sources_list) != 0:
                        for sub_source in sub_sources_list:
                            sources_res = json.loads(serializers.serialize("json", models.sub_sources.objects.filter(
                                sub_source_id=sub_source)))
                            if len(sources_res) != 0:
                                for i in sources_res:
                                    fields = i["fields"]
                                    fields['sub_source_id'] = i["pk"]
                                    sub_sources_data.append(fields)
                        sources_data["sub_sources"] = sub_sources_data
                        res.append(sources_data)
                        res = {"status": "success", "message": "sources_details get is success", "data": (res)}
                        return JsonResponse(res)
            else:
                res = {"status": "success", "message": "sources_details get is success", "data": []}
                return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def getLiveSourceCameras(request):
    try:
        event = json.loads(request.body)
        cameras_res = json.loads(
            serializers.serialize("json", models.Sources.objects.filter(source_id=event["source_id"])))
        cam_data = []
        for i in cameras_res:
            cameras = i["fields"]
            cameras = json.loads(cameras["cameras"])
            for cam in cameras:
                cam_res = json.loads(serializers.serialize("json", models.Cameras.objects.filter(camera_id=cam)))
                for i in cam_res:
                    fields = i["fields"]
                    fields['camera_id'] = i["pk"]
                    cam_data.append(fields)
            res = {"status": "success", "message": "getLiveSourceCameras get is success", "data": (cam_data)}
            return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def getSubSources(request):
    try:
        event = json.loads(request.body)
        sub_sources = json.loads(
            serializers.serialize("json", models.Sources.objects.filter(source_id=event["source_id"])))
        sub_source_data = []
        if len(sub_sources) != 0:
            for i in sub_sources:
                sub_sources_list = i["fields"]
                sub_sources_list = json.loads(sub_sources_list["sub_sources"])
                if len(sub_sources_list) != 0:
                    for sub_source in sub_sources_list:
                        sub_source_res = json.loads(
                            serializers.serialize("json", models.sub_sources.objects.filter(sub_source_id=sub_source)))
                        if len(sub_source_res) != 0:
                            for i in sub_source_res:
                                fields = i["fields"]
                                fields['sub_source_id'] = i["pk"]
                                sub_source_data.append(fields)
            res = {"status": "success", "message": "getSubSources get is success", "data": (sub_source_data)}
            return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)

@api_view(['GET', 'POST', ])
def getSubSourceItems(request):
    try:
        print("???????????????????????????????????")
        print(request)
        print(type(request))
        event = json.loads(request.body)
        print(event)
        print("???????????????????????????????????")
        jobs_res = json.loads(serializers.serialize("json", models.processed_video.objects.filter(sub_source_id=event["sub_source_id"])))
        print("***************************")
        print(jobs_res)
        print("************************************")
        res = []
        for i in jobs_res:
            print("--------", i)
            fields = i["fields"]
            res.append(fields)
        res = {
            "status": "success",
            "message": "Jobs get is success",
            "data": (res)
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)

@api_view(['GET', 'POST', ])
def sources_update(request):
    try:
        request_json = json.loads(request.body)
        event = request_json["data"]
        if event["source_type"] == "Live":
            Sources_update = models.Sources(
                source_id=event["source_id"],
                source_name=event["source_name"],
                source_type=event["source_type"],
                cameras=json.dumps(event["cameras"]),
                sub_sources=event["sub_sources"]
            )
            Sources_update.save()
            res = {"status": "success", "message": "Sources update successfully", "data": event}
            return JsonResponse(res)
        elif event["source_type"] == "Video":  # and event["source_type"]=="Image":
            sub_sources = event["sub_sources"]
            sub_sources_res = sub_sources_create(sub_sources)
            if sub_sources_res["status"] == "success":
                Sources_sub_update = models.Sources(
                    source_id=event["source_id"],
                    source_name=event["source_name"],
                    source_type=event["source_type"],
                    cameras=event["cameras"],
                    sub_sources=json.dumps(sub_sources_res["sub_sources_ids"])
                )
                Sources_sub_update.save()
                event['source_id'] = event["source_id"]
                event["sub_sources"] = sub_sources_res["data"]
                res = {"status": "success", "message": "sources update successfully", "data": event}
                return JsonResponse(res)
            else:
                res = {"status": "success", "message": "sources update successfully", }
                return JsonResponse(res)
        else:
            res = {"status": "failed", "message": sub_sources_res["message"]}
            return JsonResponse(res)
    except Exception as e:
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


def sub_sources_update(eventdata):
    try:
        final_eventdata = []
        sub_sources_ids = []
        for event in eventdata:
            sub_sources_update = models.sub_sources(
                sub_source_id=event["sub_source_id"],
                sub_source_name=event["sub_source_name"],
                folder_path=event["folder_path"])
            sub_sources_update.save()
            final_eventdata.append(event)
            sub_sources_ids.append(event["sub_source_id"])
            print(event, "ooooooooooooooooooooooooo")
        res = {"status": "success", "message": "sub_sources update successfully", "data": event,
               "sub_sources_ids": sub_sources_ids}
        return (res)
    except Exception as e:
        res = {"status": "failed", "message": str(e)}
        return (res)


# cameras
@api_view(['GET', 'POST', ])
def cameras_create(request):
    try:
        #
        request_json = json.loads(request.body)
        event = request_json["data"]
        current_date = datetime.datetime.now()
        Id_val = current_date.strftime("%Y%m%d%H%M%S")
        print("-------------->", Id_val)
        cameras_create = models.Cameras(
            camera_id=Id_val,
            camera_name=event["camera_name"],
            url=event["url"],
            location=event["location"],
            latitude=event["latitude"],
            longitude=event["longitude"],
        )
        cameras_create.save()
        event['camera_id'] = Id_val
        res = {"status": "success", "message": "cameras created successfully", "data": event}
        return JsonResponse(res)
    except Exception as e:
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def cameras_get(request):
    try:
        groups_res = json.loads(serializers.serialize("json", models.Cameras.objects.all()))
        res = []
        for i in groups_res:
            print("--------", i)
            fields = i["fields"]
            fields['camera_id'] = i["pk"]
            res.append(fields)
        res = {
            "status": "success",
            "message": "cameras get is success",
            "data": (res)
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)

    # Groups


@api_view(['GET', 'POST', ])
def groups_create(request):
    try:
        #
        request_json = json.loads(request.body)
        event = request_json["data"]
        current_date = datetime.datetime.now()
        Id_val = current_date.strftime("%Y%m%d%H%M%S")
        Sources_create = models.Groups(
            groups_id=Id_val,
            group_name=event["group_name"])
        Sources_create.save()
        event['group_id'] = Id_val
        res = {"status": "success", "message": "Groups created successfully", "data": event}
        return JsonResponse(res)
    except Exception as e:
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def groups_get(request):
    try:
        groups_res = json.loads(serializers.serialize("json", models.Groups.objects.all()))
        res = []
        for i in groups_res:
            print("--------", i)
            fields = i["fields"]
            fields['group_id'] = i["pk"]
            res.append(fields)
        res = {
            "status": "success",
            "message": "Groups get is success",
            "data": (res)
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)

    # Jobs
#"[job,jobname]"


def send_message(queue,msg):
    import pika
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters('10.99.33.140', credentials=credentials, virtual_host='example' , heartbeat=10)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=False)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(msg))
    connection.close()

@api_view(['GET', 'POST', ])
def jobs_create(request):
    try:
        request_json = json.loads(request.body)
        event = request_json["data"]
        current_date = datetime.datetime.now()
        Id_val = current_date.strftime("%Y%m%d%H%M%S")
        print("---==============---event----====================------>", event)
        job_id=Id_val
        job_name=event["job_name"]
        recurrence=event["recurrence"]
        Jobs_create = models.Jobs(
            job_id=Id_val,
            job_name=event["job_name"],
            recurrence=event["recurrence"],
            from_date=event["from_date"],
            to_date=event["to_date"],
            start_time=event["start_time"],
            sme_alert=event["sme_alert"],
            email_alert=event["email_alert"],
            function_id=event["function"],
            source_id=event["source"],
            group_id=event["group"]
        )
        # event["group"]
        Jobs_create.save()
        #print("----------------",from_date)
        start_date=event["from_date"]
        current_date = datetime.datetime.now()
        print("821")
        today = current_date.strftime("%Y-%m-%d")
        #update()
        #restart()
        kwargs={'Jobid': str(Id_val), 'JobName': event["job_name"], 'Functionid': event["function"], 'SourceID': event["source"], 'SourceType': "Video"}
        

        Jobid= job_id
        JobName= job_name
        source_id= event["source"]

        source_obj = models.Sources.objects.get(source_id=event["source"])
        print("832")
        sub_source_id=source_obj.sub_sources
        # sub_source_name='test'
        # sub_source_path='./Input/sources/vid1'
        # model_id=20220426192548
        # Functiontype='Live'
        # list_lables= ['car', 'person', 'truck']
        # rtsp_url="rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"
        # camera_name="cam1"
        # camera_id=1234

        # msg_string = {'Jobid': str(Jobid), 'JobName': JobName, 'sub_source_name': sub_source_name, 'sub_source_path': sub_source_path, 'model_id': model_id, 'Functiontype': 'Video', 'list_labels' :list_lables, 'source_id': source_id, 'sub_source_id': sub_source_id}
        
        # data fromm table
        print("847")
        flto = models.Function_lto.objects.filter(function_id=event["function"]).values_list('label__label_id',flat=True)
        print("flto",flto)
        model_ids = models.Model_labels.objects.filter(label_id__in=flto).values_list('model__model_id',flat=True).distinct()
        print("model_ids",model_ids)
        print(sub_source_id)
        for item in model_ids:
        # for item in jobs_create.function.function_lto_set.values_list('label__model_id'):
            print(source_obj.cameras)
            for jitem in eval(source_obj.cameras):
                print(item,jitem)
                print("850")
                source_id= event["source"]
                model_id = item
                Jobid= job_id
                print("853")
                JobName= job_name
                rtsp_url= models.Cameras.objects.get(id=jitem).url
                camera_name = models.Cameras.objects.get(id=jitem).camera_name
                camera_id = jitem
                print("859")
                list_lables= [i for i in models.Function_lto.objects.filter(function_id=event["function"]).values_list('label__label_name',flat=True)]
                print("861")
                Functiontype= "live"
                #sourcetype=models.Sources.objects.get(source_id=event["source"])
                ssource = ""
                print(865)
                sourcetype = "Live" #source_obj.type
                sub_source_id=jitem # list of ids
                print(868) 
                sub_source_name = "ssource.sub_source_name"
                sub_source_path = "ssource.folder_path" 
        
                print("865")
                msg_string = {'Jobid': str(Jobid), 'JobName': str(JobName), 'sub_source_name': str(sub_source_name), 
                'sub_source_path': str(sub_source_path), 'model_id': str(model_id), 'Functiontype': 'Live',
                 'list_labels' :str(list_lables), 'source_id': str(source_id), 'sub_source_id': str(sub_source_id),
                 'rtsp_url':rtsp_url, 'camera_name':camera_name, 'camera_id':camera_id, 'sourcetype' : sourcetype
                 }
                send_message('something', msg_string)    
                #send_message('worker', msg_string)    
        # end data from table
        print("369")

        # send_message('something', msg_string)        
        
        # Jobid=123
        # JobName='RSOD55'
        # sub_source_name='test'
        # sub_source_path='/usr/src/app/Worker/Input/vid1'
        # model_id=20220829064523
        # Functiontype='Video'
        # list_lables= ['car', 'person', 'truck']
        # source_id=20220907071217
        # sub_source_id=20220907071218
        # msg_string = {'Jobid': str(Jobid), 'JobName': JobName, 'sub_source_name': sub_source_name, 'sub_source_path': sub_source_path, 'model_id': model_id, 'Functiontype': 'Video', 'list_labels' :list_lables, 'source_id': source_id, 'sub_source_id': sub_source_id}
        # print("kkkkkkk", msg_string)
        if recurrence=="One Time":
            print("onetimeeeee")
            #tomorrow = datetime.datetime.utcnow() + timedelta(seconds=15)
            #print(tomorrow)
            #, eta=tomorrow 
            #Jobid, JobName, sub_source_name,sub_source_path, model_id, Functiontype, list_lables 
            msg_string = {'Jobid': str(Jobid), 'JobName': JobName, 'sub_source_name': sub_source_name, 'sub_source_path': sub_source_path, 'model_id': model_id, 'Functiontype': 'Video', 'list_labels' :list_lables, 'source_id': source_id, 'sub_source_id': sub_source_id, 'rtsp_url':rtsp_url, 'camera_name':camera_name, 'camera_id':camera_id}
            print("onetimeeeee")
            #msg_string = f"'worker.job_app', Jobid': {str(Id_val)}, 'JobName': {event['job_name']}, 'sub_source_name': {event['function']}, 'SourceID': {event['source']}, 'SourceType': 'Video']"
            #send_message("something",msg_string)
            print("done")
            # send_task('worker.job_app', kwargs={'Jobid': str(Id_val), 'JobName': event["job_name"], 'Functionid': event["function"], 'SourceID': event["source"], 'SourceType': "Video"})
        else:
            if start_date!=today:
                print("nottoday")
                days_to_seconds=eta_days(start_date, today)
                days_to_seconds=20
                eta_val = datetime.datetime.utcnow() + timedelta(seconds=days_to_seconds)
                print("Job will start in {0} days".format(days_to_seconds))
                send_task('worker.job_app', kwargs={'Jobid': str(Id_val), 'JobName': event["job_name"], 'Functionid': event["function"], 'SourceID': event["source"], 'SourceType': "Video"}, eta=eta_val, expires=40)
                update_json(job_id,job_name,recurrence)
            else:
                print("today")
                #days_to_seconds=eta_days(start_date, today)
                days_to_seconds=20
                eta_val = datetime.datetime.utcnow() + timedelta(seconds=days_to_seconds)
                send_task('worker.job_app', kwargs={'Jobid': str(Id_val), 'JobName': event["job_name"], 'Functionid': event["function"], 'SourceID': event["source"], 'SourceType': "Video"}, eta=eta_val, expires=40)

                update_json(job_id,job_name,recurrence, kwargs)


        event['job_id'] = Id_val
        res = {"status": "success", "message": "Jobs created successfully", "data": event}
        return JsonResponse(res)
    except Exception as e:
        print("error:", e)
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def jobs_get(request):
    try:
        jobs_res = json.loads(serializers.serialize("json", models.Jobs.objects.all()))
        res = []
        for i in jobs_res:
            print("--------", i)
            fields = i["fields"]
            fields['job_id'] = i["pk"]
            res.append(fields)
        res = {
            "status": "success",
            "message": "Jobs get is success",
            "data": (res)
        }

        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def jobs_detailes(request):
    # Read a specific entry:
    print("eventttttt", request)
    event = json.loads(request.body)
    # print("eventttttt", event)
    try:

        # print(event)
        # print("======")
        job_id = event['job_id']
        print(job_id)

        jobs_res = json.loads(serializers.serialize("json", models.Jobs.objects.filter(job_id=job_id)))
        # print("========================",jobs_res)
        res = []
        for i in jobs_res:
            print("--------", i)
            fields = i["fields"]
            fields['job_id'] = i["pk"]
            res.append(fields)
        res = {
            "status": "success",
            "message": "Jobs get is success",
            "data": (res)
        }
        print(res)
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)


'''
    res = {
            "status":"success",
            "message":"success"
            }  
    return JsonResponse(res)'''


@api_view(['GET', 'POST', ])
def jobs_delete(request):
    # Read a specific entry:
    print(request)
    event = json.loads(request.body)
    try:
        #print(event["job_id"])
        #jobs_re= models.processed_video.objects.get(job=event["job_id"])
        #path=jobs_re.path
        #a=os.path.split(path)
        #shutil.rmtree(a)
        #print("|||||||||||||||||||||||||||||||||||||||||||")
        #print(type(path))
        #print(path)
        #print("|||||||||||||||||||||||||||||||||||||||")

        # _dir='/usr/src/vizsense_volume/Analysis/models/'
        # _dir = os.path.join(_dir,'%s_' %model_name )
        #print(_dir)
        # shutil.rmtree(_dir)
        jobs_res = models.Jobs.objects.filter(job_id=event["job_id"]).delete()
        res = {
            "status": "success",
            "message": "Delete job is success"
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def jobs_update(request):
    try:
        request_json = json.loads(request.body)
        event = request_json["data"]
        Jobs_create = models.Jobs(
            job_id=event["job_id"],
            job_name=event["job_name"],
            recurrence=event["recurrence"],
            from_date=event["from_date"],
            to_date=event["to_date"],
            start_time=event["start_time"],
            sme_alert=event["sme_alert"],
            email_alert=event["email_alert"],
            function_id=event["function"],
            source_id=event["source"],
            group_id=event["group"]
        )
        # event["group"]
        Jobs_create.save()

  


        res = {"status": "success", "message": "Jobs Updated successfully"}
        return JsonResponse(res)
    except Exception as e:
        print("error:", e)
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def viewJob(request):
    try:
        event = json.loads(request.body)
        print("test")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(event)
        job_list=event["job_id"]
        print(job_list)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")                                                                         
        viewJob_res = json.loads(
            serializers.serialize("json", models.Sources.objects.filter(source_id=event["source_id"])))
        # print(viewJob_res)
        print(":::::::::::::::::::::::::::::::::::::::")
        res = []
        for i in viewJob_res:
            if len(i) != 0:
                sources_data = i["fields"]
                print("\\\\\\\\\\\\\\\\\\")
                print(sources_data)
                print(1099)
                if sources_data["source_type"] == "Live":
                    cameras_list = json.loads(sources_data["cameras"])
                    cam_data = []
                    if len(cameras_list) != 0:
                        for cam in cameras_list:
                            sources_res = json.loads(
                                serializers.serialize("json", models.Cameras.objects.filter(id=cam)))
                            if len(sources_res) != 0:
                                for i in sources_res:
                                    fields = i["fields"]
                                    fields['id'] = i["pk"]
                                    fields['name'] = fields["camera_name"] 
                                    fields['path'] = fields["url"]
                                    try:
                                        timestamp = int(time.time())
                                        # fields['path'] = models.processed_video.objects.filter(sub_source=i["pk"]).last().path.split("history")[0] + "live/live.webM"
                                        vid_file = models.processed_video.objects.filter(sub_source=i["pk"]).last().path.split("history")[0] + "live/live.webM"
                                        destination = f"/usr/src/app/app/AnalyticsPlatformApi/static/img/{str(timestamp)}_live.webM"
                                        shutil.copyfile(vid_file, destination)
                                        fields['path'] = f"http://10.109.144.23:8000/static/img/{str(timestamp)}_live.webM"

                                    except Exception as e:
                                        print("error from 1116e",str(e))
                                        pass
                                    del fields["camera_name"]
                                    cam_data.append(fields)
                    sources_data["cameras"] = cam_data
                    res.append(sources_data)
                    res = {"status": "success", "message": "sources_details get is success",
                           "source_type": sources_data["source_type"], "data": (cam_data)}
                    return JsonResponse(res)
                elif sources_data["source_type"] == "Video":
                    print("saisaivideo")
                    sub_sources_list = json.loads(sources_data["sub_sources"])
                    print("-----------")
                    # print(job_sources_list)
                    print(sub_sources_list)
                    print("---------------")
                    sub_sources_data = []
                    if len(sub_sources_list) != 0:
                        print(sub_sources_list)
                        for sub_source in sub_sources_list:
                            print(sub_source)
                            sources_res = json.loads(serializers.serialize("json", models.processed_video.objects.filter(
                                sub_source_id=sub_source )))
                            print("=====================")
                            print("++++++++++++++++++++++++++++++++++++")
                            print(sources_res)
                            print("=====================================")
                            if len(sources_res) != 0:
                                for i in sources_res:
                                    print("|||||||||||")
                                    print(i)
                                    print("|||||||||||||")
                                    fields = i["fields"]
                                    print("============")
                                    print(fields)
                                    jj=fields["job"]
                                    sour=fields["sub_source"]
                                    print(sour)
                                    print(type(sour))
                                    sub_source=int(sub_source)
                                    print(type(sub_source))
                                    print(jj)
                                    print(type(jj))
                                    job_list=int(job_list)
                                    print(type(job_list))
                                    if (jj == job_list) and (sour == sub_source):
                                        print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
                                    
                                        video_path=fields["path"]
                                        print(video_path)
                                        aa=os.path.split(video_path)
                                        aaa=list(aa)
                                        filename=aaa[1]
                                        print(filename)
                                        #_dire="/home/user/vat/VAT_latest/app/AnalyticsPlatformApi/static/img/3"
                                        _dire="./AnalyticsPlatformApi/static/img/3"
                                        _dir="static/img/3"
                                        shutil.copy(video_path, _dire)
                                        pp = os.path.join(_dir, filename )
                                        print("=====")
                                        print(pp)
                                        print("=======")
                                        
                                        print("=================================")
                                        fields['id'] = i["pk"]
                                        fields['name'] = fields["video_file_name"]
                                        fields['path'] =pp 
                                        sub_sources_data.append(fields)
                                        sources_data["sub_sources"] = sub_sources_data
                                        res.append(sources_data)
                                        print("+++++===========================+++++++++++++")
                                        print(res)
                                        print("+++++++++++++++++++++========================")
                                    else:
                                        print("saisaisaisasiasiasi")
                        res = {"status": "success", "message": "sources_details get is success",
                               "source_type": sources_data["source_type"], "data": (sub_sources_data)}
                        return JsonResponse(res)
            else:
                res = {"status": "failed", "message": "view Job get is Not Avilabel for this ID", "data": []}
                return JsonResponse(res)
    except Exception as e:
        print("error:", e)
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


# Analytics

@api_view(['GET', 'POST', ])
def analytics_tab(request):
    try:
        print(request)
        request_json = json.loads(request.body)
        print("***************************************")
        print(request_json)
        print("**** *************************************")

        jobid = request_json["data"]["job_id"]
        source_type = request_json["data"]["source_type"]
        source_id = request_json["data"]["source_id"]
        sub_source_id = request_json["data"]["sub_source_id"]
        # live_camera_id=request_json["data"]["live_camera_id"]
        start_date = request_json["data"]["start_date"]
        start_date = str(start_date) + " 00:00:00"
        start_date = "'%s'" % start_date
        end_date = request_json["data"]["end_date"]
        end_date = str(end_date) + " 23:59:59"
        end_date = "'%s'" % end_date

        print(jobid)
        print(source_type)
        print(source_id)
        print(sub_source_id)
        # print(live_camera_id)
        print(start_date)
        print(end_date)

        cls = database_function()
        # if source_type == "Live":
        #     sub_source_id= live_camera_id

        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        print(connection)
        # postgreSQL_select_Query = 'SELECT * FROM "log" WHERE jobid={0} AND timestamp BETWEEN {1} AND {2} '.format(jobid, start_date, end_date)
        # postgreSQL_summary_Query='SELECT SUM(DISTINCT totalframes) AS totalframes_processed, COUNT(*) labels_detected  FROM "log" WHERE jobid={0} AND timestamp BETWEEN {1} AND {2} '.format(jobid, start_date, end_date)
        # postgreSQL_select_Query = 'SELECT * FROM "log" WHERE jobid={0} AND sourceid={3} AND timestamp BETWEEN {1} AND {2} '.format(jobid, start_date, end_date, source_id)

        if sub_source_id == "combined" or sub_source_id == "all":
            postgreSQL_select_Query = 'SELECT * FROM "log" WHERE jobid={0} AND timestamp BETWEEN {1} AND {2} '.format(
                jobid, start_date, end_date, source_id)
            postgreSQL_summary_Query = 'SELECT SUM(DISTINCT totalframes) AS totalframes_processed, COUNT(*) labels_detected  FROM "log" WHERE jobid={0} AND timestamp BETWEEN {1} AND {2} '.format(
                jobid, start_date, end_date)

            print("postgreSQL_select_Query",postgreSQL_select_Query)
        else:
            postgreSQL_select_Query = 'SELECT * FROM "log" WHERE jobid={0} AND sub_sourceid={3} AND timestamp BETWEEN {1} AND {2} '.format(
                jobid, start_date, end_date, sub_source_id)
            postgreSQL_summary_Query = 'SELECT SUM(DISTINCT totalframes) AS totalframes_processed, COUNT(*) labels_detected  FROM "log"  WHERE jobid={0} AND sub_sourceid={3} AND timestamp BETWEEN {1} AND {2} '.format(
                jobid, start_date, end_date, sub_source_id)

        print("postgreSQL_select_Query",postgreSQL_select_Query)
        cursor.execute(postgreSQL_select_Query)
        query_tuple = cursor.fetchall()
        keys = (
        "detectionid", "functiontype", "objectid", "filename", "framecount", "totalframes", "classid", "classname",
        "coordinates", "timestamp", "job_id"
        , "source_id", "sub_source_id", "sub_souce_name", "retscore", "model_label_id")
        list_of_all_dict = [dict(zip(keys, values)) for values in query_tuple]
        #print("--", list_of_all_dict)
        cursor.execute(postgreSQL_summary_Query)
        summary_tuple = cursor.fetchone()
        keys = ("totalframes_processed", "labels_detected")
        list_of_summary_dict = dict(zip(keys, summary_tuple))
        print("################################")
        print(list_of_summary_dict)
        print("####################################")
        print(source_id)
        #subsourcename = cls.get_source_name(source_id)
        #print(subsourcename)
        chartdata = []

        # print(chartdata)
        res = {"message": "success", "status": "success", "chartData": list_of_all_dict,
               "summary": list_of_summary_dict}
        print(res)
        print(JsonResponse(res))
        return JsonResponse(res)

    except Exception as e:
        res = {"message": str(e), "status": "failed"}
        return JsonResponse(res)

    # Tasks


@api_view(['GET', 'POST', ])
def task_create(request):
    try:
        request_json = json.loads(request.body)
        event = request_json["data"]
        current_date = datetime.datetime.now()
        Id_val = current_date.strftime("%Y%m%d%H%M%S")
        print("---==============---event----====================------>", event)
        task_create = models.Tasks(
            tasks_id=Id_val,
            task_name=event["task_name"]
        )
        # event["group"]
        task_create.save()
        event['tasks_id'] = Id_val
        res = {"status": "success", "message": "Task created successfully", "data": event}
        return JsonResponse(res)
    except Exception as e:
        print("error:", e)
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def task_get(request):
    try:
        task_res = json.loads(serializers.serialize("json", models.Tasks.objects.all()))
        res = []
        for i in task_res:
            print("--------", i)
            fields = i["fields"]
            fields['task_id'] = i["pk"]
            res.append(fields)
        res = {
            "status": "success",
            "message": "Tasks get is success",
            "data": (res)
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)

    # Operations


@api_view(['GET', 'POST', ])
def operations_create(request):
    try:
        request_json = json.loads(request.body)
        event = request_json["data"]
        current_date = datetime.datetime.now()
        Id_val = current_date.strftime("%Y%m%d%H%M%S")
        print("---==============---event----====================------>", event)
        task_create = models.Operations(
            operation_id=Id_val, operation_name=event["operation_name"]
        )
        # event["group"]
        task_create.save()
        event['operation_id'] = Id_val
        res = {"status": "success", "message": "operations created successfully", "data": event}
        return JsonResponse(res)
    except Exception as e:
        print("error:", e)
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def operations_get(request):
    try:
        operations_res = json.loads(serializers.serialize("json", models.Operations.objects.all()))
        res = []
        for i in operations_res:
            print("--------", i)
            fields = i["fields"]
            fields['operation_id'] = i["pk"]
            res.append(fields)
        res = {
            "status": "success",
            "message": "operations get is success",
            "data": (res)
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)



@api_view(['GET', 'POST', ])
def models_create(request):
    try:
        print(request.data)
        print(request.FILES)
        modelFormData = request.data.get('data')
        modelFormData = json.loads(modelFormData)
        model_name = modelFormData["model_name"]
        architecture = modelFormData["architecture"]
        comments = modelFormData["comments"]
        print("Save Model Details: modelName: ", model_name, "architecture: ", architecture, "comments: ", comments)
        event= {"model_name": model_name, "architecture": architecture, "comments": comments, "status": "ACTIVE"}
        ##################################################################################

        current_date = datetime.datetime.now()
        Id_val = int(current_date.strftime("%Y%m%d%H%M%S"))
    #########################################################################################
        if request.method=='POST':
            uploaded_file=request.FILES['label_files[]']
            _dir='/usr/src/vizsense_volume/Analysis/models'
            print("_dirrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr", _dir)
            s=model_name+"_"+str(Id_val)
            _dir = os.path.join(_dir,'%s' %s )
            _dir=os.path.join(_dir ,'1')
            fs=FileSystemStorage(_dir)
            fs.save(uploaded_file.name,uploaded_file)
            print(_dir)
            s=os.path.join(_dir, "/", uploaded_file.name)
            filepath=_dir+s
            print(filepath)
            print(s)
            if not os.path.exists(_dir):
                os.makedirs(_dir)
            ####################################
            upload_file=request.FILES['model_files[]']
            _dir='/usr/src/vizsense_volume/Analysis/models'
            s=model_name+"_"+str(Id_val)
            _dir = os.path.join(_dir,'%s' %s )
            #_dir = os.path.join(_dir,'%s_' %model_name)
            _dir=os.path.join(_dir ,'1')
            fs=FileSystemStorage(_dir)
            fs.save(upload_file.name,upload_file)
            print(_dir)
            a=os.path.join(_dir, "/", upload_file.name)
            modelpath=_dir+a
            # # s=os.path.abspath(uploade_file.name)
            # # s=_dir+/+uploaded_file.name
            print(modelpath)
            model_path=_dir
            #model_path=r'/home/user/RSRObjectdetection/SHC/Inference/RSRModels/ssd_mobilenet_v1_coco_2018_01_28/saved_model'
            #stream = os.popen('saved_model_cli show --dir %s --all' % (model_path))
            #output = stream.read()
            #print("op", output)
            #outputstr=str(output)
            #print(("""%s""" % (outputstr)))
            #signature=outputstr.splitlines()
           # signature=signature[3]
            #print("---", signature[3])
            #print("--",signature)
            signature='serving_default' #signature.split("'")[1]

            print(signature)
            # print(s)
            # if not os.path.exists(_dir):
            #     os.makedirs(_dir)
            
    ###############################################################################################################################
        current_date = datetime.datetime.now()
        Id_val = int(current_date.strftime("%Y%m%d%H%M%S"))
       
        print("---==============---event----====================------>", event)
        

        models_create = models.Models(
            model_id=Id_val,
            model_name=event["model_name"],
            architecture=event["architecture"],
            model_specname=model_name+"_"+str(Id_val),
            model_signature=signature,
            label_file_path=filepath,
            model_file_path=modelpath,
            comments=event["comments"]            
        )
        models_create.save()
        print("after")
        event['model_id'] = Id_val
        ########################################################################################
        item_id = None
        item_name = None
        item_label=None
        item = {}
        lable_list=[]
        label_name=None
        model_label_id=None
        model_id=None
        with open(filepath, "r") as file:
            for line in file:
                line.replace(" ", "")
                if line == "item{":
                    pass
                elif line == "}":
                    pass
                elif "id" in line:
                    item_id = int(line.split(":", 1)[1].strip())
                    item["model_label_id"]=item_id
                elif "display_name" in line:
                    item_name = line.split(":", 1)[1].replace("'","").strip()
                    item_name=item_name.replace('"','')
                    print(item_name)
                    item["label_name"] = item_name
                    val={"label_name":item["label_name"],"model_id":event["model_id"],"model_label_id":item["model_label_id"]}
                    lable_list.append(val)
        labels_tasks_res = Model_labels_create(lable_list)
        #update_models_config(s)
                                                                                                                                               
        res = {"status": "success", "message": "Jobs created successfully", "data": event}
        return JsonResponse(res)
    except Exception as e:
        print("error:", e)
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def models_get(request):
    try:
        operations_res = json.loads(serializers.serialize("json", models.Models.objects.all()))
        res = []
        for i in operations_res:
            print("--------", i)
            fields = i["fields"]
            fields['model_id'] = i["pk"]
            res.append(fields)
        res = {
            "status": "success",
            "message": "models get is success",
            "data": (res)
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)
@api_view(['GET', 'POST', ])
def models_update(request):
    try:
        
        print("ssssssssssssss")
        print(request.data)
        print(type(request.data))
        sp=( {k: v[0] if len(v) == 1 else v for k, v in request.data.lists()})
        print("dddddddddddddd")
        print(sp)
        print(type(sp))
        b=request.FILES
        print(b)
        print(type(b))
        # if sp["data"] !=0 and request.FILES["label_files[]"] == 0:
        #     print("sai")
        if request.FILES== {}:
            sss = sp["data"]
            event=ast.literal_eval(sss)
            print(event)
            pp=event["label_file_path"]
            mp=event["model_file_path"]
            m=os.path.split(mp)
            mpp=list(m)
            modelname=mpp[1]
            model_name=event["model_name"]
            print(pp)
            p=os.path.split(pp)
            ppp=list(p)
            split_path=ppp[0]
            lable_name=ppp[1]
            _dir='/usr/src/vizsense_volume/Analysis/models/'
            _dir = os.path.join(_dir,'%s_' %model_name )
            _dir=os.path.join(_dir ,'1')
            s=os.path.join(_dir, "/",lable_name)
            l=os.path.join(_dir, "/",modelname)
            filepath=_dir+s
            modelpath=_dir+l
            print(filepath)
            print(modelpath)  #\43            print(_dir,"+++++++++")
            shutil.move(split_path, _dir)
            # os.rename(split_path, _dir)
            print(type(event))

            models_update = models.Models(
                model_id=event["model_id"],
                model_name=model_name,
                architecture=event["architecture"],
                model_specname=event["model_specname"],
                model_signature=event["model_signature"],
                label_file_path=filepath,
                model_file_path=modelpath,
                comments=event["comments"]            
            )
            models_update.save()
            print("After sai")

            print("reddy")
        else:
            sss = sp["data"]
            event=ast.literal_eval(sss)
            print(event)
            model_name=event["model_name"]
            model_file_path=event["model_file_path"]
            label_file_path=event["label_file_path"]
            aa=os.path.split(label_file_path)
            aa=list(aa)
            aaa=aa[0]
            _dire='/usr/src/vizsense_volume/Analysis/models/'
            _dire = os.path.join(_dire,'%s_' %model_name )
            _dire=os.path.join(_dire ,'2')
            print("=||||||||||||||==========")
            print(aaa)
            print(_dire)
            print("============")
            shutil.move(aaa, _dire)
            # if not os.path.exists(_dire):
            #         os.makedirs(_dire)
            print("===========")
            print(aaa)
            print(_dire)
            print("============")
            
            print(type(event))
            if request.method=='POST':
                uploaded_file=request.FILES['label_files[]']
                _dir='/usr/src/vizsense_volume/Analysis/models/'
                _dir = os.path.join(_dir,'%s_' %model_name )
                _dir=os.path.join(_dir ,'1')
                fs=FileSystemStorage(_dir)
                fs.save(uploaded_file.name,uploaded_file)
                print(_dir)
                s=os.path.join(_dir, "/", uploaded_file.name)
                filepath=_dir+s
                print(filepath)
                print(s)
                if not os.path.exists(_dir):
                    os.makedirs(_dir)
                ####################################
                upload_file=request.FILES['model_files[]']
                _dir='/usr/src/vizsense_volume/Analysis/models/'
                s=model_name+"_" #+str(Id_val)
                _dir = os.path.join(_dir,'%s' %s )
                #_dir = os.path.join(_dir,'%s_' %model_name)
                _dir=os.path.join(_dir ,'1')
                fs=FileSystemStorage(_dir)
                fs.save(upload_file.name,upload_file)
                print(_dir)
                a=os.path.join(_dir, "/", upload_file.name)
                modelpath=_dir+a
                # # s=os.path.abspath(uploade_file.name)
                # # s=_dir+/+uploaded_file.name
                print(modelpath)
                model_path=_dir
                #model_path=r'/home/user/RSRObjectdetection/SHC/Inference/RSRModels/ssd_mobilenet_v1_coco_2018_01_28/saved_model'
                stream = os.popen('saved_model_cli show --dir %s --all' % (model_path))
                output = stream.read()
                #print("op", output)
                outputstr=str(output)
                #print(("""%s""" % (outputstr)))
                signature=outputstr.splitlines()
                signature=signature[3]
                #print("---", signature[3])
                #print("--",signature)
                signature=signature.split("'")[1]
                print(signature)
                # print(s)
                # if not os.path.exists(_dir):
                #     os.makedirs(_dir)
                
        ###############################################################################################################################
            #current_date = datetime.datetime.now()
            #Id_val = int(current_date.strftime("%Y%m%d%H%M%S"))
        
            print("---==============---event----====================------>", event)
            

            models_update = models.Models(
                model_id=event["model_id"],
                model_name=model_name,
                architecture=event["architecture"],
                model_specname=model_name+"_", #+str(Id_val),
                model_signature=signature,
                label_file_path=filepath,
                model_file_path=modelpath,
                comments=event["comments"]            
            )
            models_update.save()
            print("after")
            ########################################################################################
            item_id = None
            item_name = None
            item_label=None
            item = {}
            lable_list=[]
            label_name=None
            model_label_id=None
            model_id=None
            with open(filepath, "r") as file:
                for line in file:
                    line.replace(" ", "")
                    if line == "item{":
                        pass
                    elif line == "}":
                        pass
                    elif "id" in line:
                        item_id = int(line.split(":", 1)[1].strip())
                        item["model_label_id"]=item_id
                    elif "display_name" in line:
                        item_name = line.split(":", 1)[1].replace("'","").strip()
                        item_name=item_name.replace('"','')
                        print(item_name)
                        item["label_name"] = item_name
                        
                        val={"label_name":item["label_name"],"model_id":event["model_id"],"model_label_id":item["model_label_id"]}
                        lable_list.append(val)
            labels_tasks_res = Model_labels_create(lable_list)

            print("sai")


        
        # ##################################################################################
                                                                                                                                            
        res = {"status": "success", "message": "Jobs created successfully", "data":event }
        return JsonResponse(res)
    except Exception as e:
        print("error:", e)
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)



import os
import sys
import shutil

@api_view(['GET', 'POST', ])
def models_delete(request):
    # Read a specific entry:
    print(request)
    event = request.data
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(event)
    print(type(event))
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    
    
    try:
        jobs_re= models.Models.objects.get(model_id=event["model_id"])
        path=jobs_re.label_file_path
        print(type(path))
        print(path)
        model_name=jobs_re.model_name
        print(model_name)

        _dir='/usr/src/vizsense_volume/Analysis/models/'
        _dir = os.path.join(_dir,'%s_' %model_name )
        print(_dir)
        shutil.rmtree(_dir)
        # os.rmdir(_dir)
        # os.remove(path)

        # if len(jobs_re.label_file_path) > 0:
        #     print(">>>>>>")
        #     os.remove(jobs_re.label_file_path.a)
        jobs_res = models.Models.objects.filter(model_id=event["model_id"]).delete()
        res = {
            "status": "success",
            "message": "Delete job is success"
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)
@api_view(['GET', 'POST', ])
def models_detailes(request):

    # print( request)
    print(type(request))
    print("????????????????????????????")
    print(request.body)
    print("?????????????????????????????????")
    # print(request.data)
    print("///////////////////////////////////////")

    event = json.loads(request.body)
    # print("eventttttt", event)
    try:

        # print(event)
        # print("======")
        model_id = event['model_id']
        print(model_id)

        jobs_res = json.loads(serializers.serialize("json", models.Models.objects.filter(model_id=model_id)))
        # print("========================",jobs_res)
        res = []
        for i in jobs_res:
            print("--------", i)
            fields = i["fields"]
            fields['model_id'] = i["pk"]
            res.append(fields)
        res = {
            "status": "success",
            "message": "Jobs get is success",
            "data": (res)
        }
        print(res)
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)

def Model_labels_create(lable_list):
    try:
        # print(lable_list)
        print(type(lable_list))
        current_date = datetime.datetime.now()
        Id_val = current_date.strftime("%Y%m%d%H%M%S")

        for event in lable_list:
            # date = datetime(2020, 2, 20)
            # date += timedelta(days=1)
            Id_val=str(int(Id_val)+1)
            # current_date += timedelta(days=1)
            print("---==============---event----====================------>",event)
            model_labels_bulk_create = models.Model_labels(
                        model_id=event["model_id"],
                        label_name=event["label_name"],
                        label_id=Id_val,
                        model_label_id=event["model_label_id"]
            )
            model_labels_bulk_create.save()
            event['label_id'] = Id_val
            print("label after")
            print(Id_val)
            # event['label_id'] = Id_val
        res = {"status": "success", "message": "Model labels create created successfully"}
        return JsonResponse(res)
    except Exception as e:
        print("error:", e)
        res = {"status": "failed", "message": str(e)}
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def labels_get(request):
    try:
        #    event=json.loads(request.body)
        #    labels_res = json.loads(serializers.serialize("json",models.Model_labels.objects.filter(model_id=event["model_id"])))
        labels_res = json.loads(serializers.serialize("json", models.Model_labels.objects.all()))
        res = []
        for i in labels_res:
            print("--------", i)
            fields = i["fields"]
            fields['label_id'] = i["pk"]
            res.append(fields)
        res = {
            "status": "success",
            "message": "labels get is success",
            "data": (res)
        }
        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res)


@api_view(['GET', 'POST', ])
def celery_beat(request):
    try:
        jobs_res = json.loads(serializers.serialize("json", models.Jobs.objects.all()))
        res = []
        for i in jobs_res:
            if len(i) != 0:
                sources_data = i["fields"]
                if sources_data["recurrence"] == "Weekly":
                    sub_data = []
                    fields = i["fields"]
                    fields['date'] = fields['from_date']
                    fields['time'] = fields['start_time']
                    sub_data.append(fields)
                    res.append(sub_data)
                    res = {"status": "success", "recurrence": sources_data["recurrence"], "data": (sub_data)}
                    return JsonResponse(res)

                elif sources_data["recurrence"] == "Monthly":
                    sub_data = []
                    fields = i["fields"]
                    fields['date'] = fields['from_date']
                    fields['time'] = fields['start_time']
                    sub_data.append(fields)
                    res.append(sub_data)
                    res = {"status": "success", "recurrence": sources_data["recurrence"], "data": (sub_data)}
                    return JsonResponse(res)

                elif sources_data["recurrence"] == "Range":
                    sub_data = []
                    fields = i["fields"]
                    fields['startdate'] = fields['from_date']
                    fields['starttime'] = fields['start_time']
                    fields['enddate'] = fields['to_date']
                    sub_data.append(fields)
                    res.append(sub_data)
                    res = {"status": "success", "recurrence": sources_data["recurrence"], "data": (sub_data)}
                    return JsonResponse(res)

                elif sources_data["recurrence"] == "Continuous":
                    sub_data = []
                    fields = i["fields"]
                    fields['startdate'] = fields['from_date']
                    fields['starttime'] = fields['start_time']
                    fields['enddate'] = fields['to_date']
                    sub_data.append(fields)
                    res.append(sub_data)
                    res = {"status": "success", "recurrence": sources_data["recurrence"], "data": (sub_data)}
                    return JsonResponse(res)
            else:
                res = {"status": "failed"}
                return JsonResponse(res)

        return JsonResponse(res)
    except Exception as e:
        res = {
            "status": "failed",
            "message": str(e)
        }
        return JsonResponse(res) 
