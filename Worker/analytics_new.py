from collections import Counter
from log_database import database_function

cls=database_function()

jobid=1232334
connection = psycopg2.connect(user="apex1", password="apex1", host="postgres", port="5432", database="viz")
cursor = connection.cursor() 
postgreSQL_select_Query = 'SELECT * FROM "log" WHERE jobid={0}'.format(jobid)
cursor.execute(postgreSQL_select_Query)
jobids = cursor.fetchall()
def get_list_of_dict(keys, list_of_tuples):
     list_of_dict = [dict(zip(keys, values)) for values in list_of_tuples]
     return list_of_dict
 
keys=("detectionid", "functiontype","objectid","filename","framecount","totalframes","classid","classname","coordinates","timestamp" ,"job_id"
,"source_id","sub_source_id")
list_of_all_dict=(get_list_of_dict(keys, jobids))
subsourceids=[12345, 56789]         
chartdata=[]
for id in subsourceids:
	values=[]
	subsourcename=cls.get_subbsource_name(id)
    list_of_req_dict = list(filter(lambda x:x["sub_source_id"] == id, list_of_all_dict))
    list_of_labels=[d['classname'] for d in list_of_req_dict]
    dict_label_and_count = Counter(list_of_labels)
    keys = dict_label_and_count.keys()
    vals = dict_label_and_count.values()
    keys,values = zip(*dict_label_and_count.items())                    
    keys=list(keys)
    values=list(values)
	subsourcedata={"values":values,"name":subsourcename,"labels":keys}	
	chartdata.append(subsourcedata)	

print(chartdata)
print("=========")
res = {"message":"success","status":"success","chartData":chartdata}
print(res)
#return JsonResponse(res)
