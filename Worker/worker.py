import pika
import time
import json
import os

print("startttttttt")


credentials = pika.PlainCredentials('admin', 'admin')
parameters = pika.ConnectionParameters('10.99.33.140', credentials=credentials, virtual_host='example' , heartbeat=10)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
print(' [*] Waiting for messages. To exit press CTRL+C')
print("Worker Function++++++++")

from lib.process_video import myvideoThread
from lib.process_live import myliveThread
from lib.log_database import database_function
from lib.job_status_func import status_update

  
def job_app(ch, method, properties, body): 
    print("job_app--------->")
    print(" [x] Received %r" % body) 
    #try:
    print("bodyyy", body)
    body = json.loads(body)
    Jobid = body['Jobid']
    JobName = body['JobName']
    sub_source_name=body['sub_source_name']
    sub_source_path=body['sub_source_path']
    model_id=body['model_id']
    Functiontype=body['Functiontype']
    list_lables= body['list_labels']
    sub_source_id=body['sub_source_id']
    source_id = body["source_id"]
    camera_id= body["camera_id"]
    camera_name = body["camera_name"]
    rtsp_url= body["rtsp_url"]
    sourcetype=body["sourcetype"]


    outpath='/usr/src/vizsense_volume/Analysis/Live'
    print(Jobid, JobName, sub_source_name,sub_source_path, model_id, Functiontype, list_lables)
    clss=status_update()
    clss.job_status(status="RUNNING", job_id=Jobid)
    threads = []
    Threadid=1
    port_number=5553
    print(port_number) 
    if sourcetype=="Video":
        thread = myvideoThread(Threadid, Jobid, JobName, sub_source_name,sub_source_path, model_id, list_lables, Functiontype, source_id, sub_source_id, outpath, port_number)
        port_number+=1
        thread.start()
        thread.vehdet()
        threads.append(thread)
        Threadid+=1
    elif sourcetype=="Live":
        print("Live source")
        thread = myliveThread(Threadid, Jobid, JobName, rtsp_url, model_id, list_lables, Functiontype, camera_name, camera_id,source_id, outpath, port_number)
        thread.start()
        thread.vehdet()
        threads.append(thread)
        Threadid+=1
    for t in threads:
        t.join()
    clss.job_status(status="COMPLETED", job_id=Jobid)
    print( "Exiting Main Thread")
    ch.basic_ack(delivery_tag = method.delivery_tag)
    ch.close()



channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='something', on_message_callback=job_app)
channel.start_consuming()
print("started calling app")