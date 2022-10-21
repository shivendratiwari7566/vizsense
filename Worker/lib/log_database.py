import psycopg2      
import json                                                                                                                                     

class database_function:

    def get_subbsource(self,Sourceid):
        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT sub_sources FROM public."Sources" WHERE Source_id={0}'.format(Sourceid)
        cursor.execute(postgreSQL_select_Query)
        sub_source_ids = cursor.fetchall()
        sub_source_ids=json.loads(sub_source_ids[0][0])
        VideoSources=[]
        for sub_source_id in sub_source_ids:
            dict={}
            postgreSQL_select_Query = 'SELECT sub_source_name,folder_path FROM public."sub_sources" WHERE sub_source_id={0}'.format(sub_source_id)
            cursor.execute(postgreSQL_select_Query)
            sub_source_names = cursor.fetchall()
            sub_source_names=sub_source_names[0]
            #name_path_tuple=get_name_path(sub_source_id)
            dict={"name":sub_source_names[0], "location":sub_source_names[1], "sub_source_id":sub_source_id}
            VideoSources.append(dict)
        print(VideoSources)
        return VideoSources


    def get_function_type(self,Functionid):
        try:
            labelids=[]
            labelnames=[]
            connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
            cursor = connection.cursor() 
            #postgreSQL_select_Query = 'SELECT * FROM public."Jobs";'            
            print(Functionid)
            postgreSQL_select_Query = 'SELECT function_type FROM public."Functions" WHERE function_id={0}'.format(Functionid)  
            cursor.execute(postgreSQL_select_Query) 
            function_type = cursor.fetchone() 
            function_type = function_type[0]
            print(function_type)
            return function_type

        except (Exception, psycopg2.Error) as error: 
            print("Failed", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


    def get_label_name(self,Functionid):
        try:
            labelids=[]
            labelnames=[]
            connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
            cursor = connection.cursor() 
            #postgreSQL_select_Query = 'SELECT * FROM public."Jobs";'            
            print(Functionid)
            postgreSQL_select_Query = 'SELECT label_id FROM public."Function_lto" WHERE function_id={0}'.format(Functionid)  
            cursor.execute(postgreSQL_select_Query) 
            label_id = cursor.fetchall() 
            print(label_id)
            for ids in label_id:
                print(ids)
                for id_value in ids:
                    print(id_value)
                    labelids.append(id_value)
            print(labelids)
            
        
		    #print(label_id)
		    #label_id = label_id[0]
		    #print(label_id)
                    
            for labelid in labelids:
                postgreSQL_select_Query = 'SELECT label_name FROM public."Model_labels" WHERE label_id={0}'.format(labelid) 
                cursor.execute(postgreSQL_select_Query) 
                label_name = cursor.fetchone()  
                print(label_name)
                label_name = label_name[0]
                print(label_name)
                labelnames.append(label_name)
            print(labelnames)
            return labelnames
  
        except (Exception, psycopg2.Error) as error: 
            print("Failed", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


    def get_model_id_from_lto(self,Functionid):
        try:
            model_id_list=[]
            connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
            cursor = connection.cursor() 
            #postgreSQL_select_Query = 'SELECT * FROM public."Jobs";'            
            print(Functionid)
            postgreSQL_select_Query = 'SELECT label_id FROM public."Function_lto" WHERE function_id={0}'.format(Functionid)  
            cursor.execute(postgreSQL_select_Query) 
            label_id = cursor.fetchall() 
            for val in label_id:
                label_id=val[0]


                postgreSQL_select_Query = 'SELECT model_id FROM public."Model_labels" WHERE label_id={0}'.format(label_id)  
                cursor.execute(postgreSQL_select_Query) 
                model_id = cursor.fetchone() 
                model_id=model_id[0]
                model_id_list.append(model_id)
                print(model_id)

            model_id_list=list(set(model_id_list))

            print(model_id_list)
            return model_id_list
  
        except (Exception, psycopg2.Error) as error: 
            print("Failed", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    
                                                                                                                                   
                                                                                                                                                
    
    def log_entry(self,detectionid, functiontype, objectid, filename, framecount, totalframes, classid, classname, coordinates, timestamp, jobid, sourceid, sub_sourceid, sub_souce_name, retscore, model_label_id):
	    try:
		    sub_sourcename=sub_souce_name
		    print("===log=====")
		    connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
		    cursor = connection.cursor() 
		    postgres_insert_query = """ INSERT INTO log VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""                                                
		    record_to_insert = (detectionid, functiontype, objectid, filename, framecount, totalframes, classid, classname, coordinates, timestamp, jobid , sourceid,  sub_sourceid, sub_sourcename, retscore, model_label_id)                                                                                                                                 
		    print(postgres_insert_query)
		    print(record_to_insert)
		    cursor.execute(postgres_insert_query, record_to_insert)
		    connection.commit()   
		    print("log values inserted successfully")

	    except (Exception, psycopg2.Error) as error: 
		    print("Failed to insert record into table", error)

	    finally:
		# closing database connection.
    		if connection:
    		    cursor.close()
    		    connection.close()
    		    print("PostgreSQL connection is closed")


    def get_subbsource_name(self,sub_source_id):
        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT sub_source_name FROM "sub_sources" WHERE sub_source_id={0}'.format(sub_source_id)
        cursor.execute(postgreSQL_select_Query)
        sub_source_name = cursor.fetchone()
        sub_source_name=sub_source_name[0]
        print(sub_source_name)
        return sub_source_name


    def get_subbsource_path(self,sub_source_id):
        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT folder_path FROM "sub_sources" WHERE sub_source_id={0}'.format(sub_source_id)
        cursor.execute(postgreSQL_select_Query)
        sub_source_path = cursor.fetchone()
        sub_source_path=sub_source_path[0]
        print(sub_source_path)
        return sub_source_name


    def get_label_id(self, label_name):
        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()

        postgreSQL_select_Query = 'SELECT label_id FROM "Model_labels" WHERE label_name={0}'.format(label_name)
        cursor.execute(postgreSQL_select_Query)
        label_id = cursor.fetchone()
        label_id=label_id[0]
        print(label_id)
        return label_id



    def get_log_row_count(self):
        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT count(*) FROM "log"'
        cursor.execute(postgreSQL_select_Query)
        row_count = cursor.fetchone()
        row_count=row_count[0]
        print(row_count)
        return row_count


    def get_log_row_count_processed_video(self):
        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT count(*) FROM "processed_video"'
        cursor.execute(postgreSQL_select_Query)
        pv_row_count = cursor.fetchone()
        pv_row_count=pv_row_count[0]
        print(pv_row_count)
        return pv_row_count

    def get_model_path(self, model_id):
        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT model_file_path FROM "Models" WHERE model_id={0}'.format(model_id)
        cursor.execute(postgreSQL_select_Query)
        model_file_path = cursor.fetchone()
        model_file_path=model_file_path[0]
        print(model_file_path)
        return model_file_path


    def get_label_name_model(self, model_label_id, model_id):
        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT label_name FROM "Model_labels" WHERE model_id={0} AND model_label_id={1}'.format(model_id, model_label_id)
        cursor.execute(postgreSQL_select_Query)
        label_name_model = cursor.fetchone()
        label_name_model=label_name_model[0]
        print(label_name_model)
        return label_name_model

    def get_model_name(self, model_id):
        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT model_name FROM "Models" WHERE model_id={0}'.format(model_id)
        cursor.execute(postgreSQL_select_Query)
        model_name = cursor.fetchone()
        model_name=model_name[0]
        print(model_name)
        return model_name

    def processed_video_entry(self,processed_video_id, video_file_name, processed_date, path, job_id, source_type, sub_source_id):
        try:
            print("===processed_video=====")
            connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
            cursor = connection.cursor() 
            postgres_insert_query = """ INSERT INTO processed_video VALUES (%s, %s, %s, %s, %s, %s, %s)"""                                                
            record_to_insert = (processed_video_id, video_file_name, processed_date, path, job_id, source_type, sub_source_id )                                                                                                    
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()   
            print("processed data inserted successfully")

        except (Exception, psycopg2.Error) as error: 
            print("Failed to insert record into table", error)

        finally:
		# closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")



#label_name="'car'"                                                                                        
#Functionid=20211126125705 
##Sourceid=20211005194713 
#sub_source_id=20211005062245

#cls=database_function()

#cls.get_label_name(Functionid)


#cls.get_function_type(Functionid)
#Sourceid=20210930053218
#cls.get_subbsource(Sourceid)
#sub_source_id=20210930053218
#cls.get_subbsource(Sourceid)
#cls.get_subbsource_path(20211127162608)
#cls.get_source_name(Sourceid)
#cls.label_id(label_name)
                                                                                          
#cls=database_function()
#Sourceid=20211127162607
#Functionid=20211005194317 
#Sourceid=20211005194713
#sub_source_id=20211005062245
#Sourceid=20210930053218
#sub_source_id=20210930053218

#cls.get_label_name(Functionid)
#cls.get_function_type(Functionid)
#cls.get_subbsource(Sourceid)
#cls.get_subbsource_name(sub_source_id)

#cls.get_log_row_count()

#model_id=20210930051456
#cls.get_model_path(model_id)

#cls.log_entry(1, 'Detection', 3, 'vid1.mp4', 54, 935, 20211126143411, 'car',  [712, 1136, 740, 1194], 2021-11-27 11:37:11, 20211127060512, 20211005194713, 20211005194714, 'vid', 77, 3)
#function_id=20211206142248
#cls.get_model_id_from_lto(function_id)

#model_id=20210930051819
#model_label_id=2

#cls.get_label_name(model_label_id, model_id)
'''
processed_video_id=2
video_file_name="vid2.mp4"
processed_date="2021-11-29 19:15:45"
path='static/img/Sub2.webM'
job_id=20211130083931

source_type="Video"
sub_source_id=20211127162609
cls.processed_video_entry(processed_video_id, video_file_name, processed_date, path, job_id,source_type, sub_source_id )


'''
