import psycopg2      
import json                                                                                                                                     

class database_function:

    def get_subbsource(self,Sourceid):
        connection = psycopg2.connect(user="apex1", password="apex1", host="postgres", port="5432", database="viz")
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
            dict={"name":sub_source_names[0], "location":sub_source_names[1]}
            VideoSources.append(dict)
        print(VideoSources)
        return VideoSources


    def get_function_type(self,Functionid):
        try:
            labelids=[]
            labelnames=[]
            connection = psycopg2.connect(user="apex1", password="apex1", host="postgres", port="5432", database="viz")
            cursor = connection.cursor() 
            #postgreSQL_select_Query = 'SELECT * FROM public."Jobs";'            
            print(Functionid)
            postgreSQL_select_Query = 'SELECT function_type FROM public."Functions" WHERE function_id={0}'.format(Functionid)  
            cursor.execute(postgreSQL_select_Query) 
            function_type = cursor.fetchone() 
            function_type = function_type[0]
            print(function_type)
            #return function_type

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
            connection = psycopg2.connect(user="apex1", password="apex1", host="postgres", port="5432", database="viz")
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
    
                                                                                                                                   
                                                                                                                                                
    
    def log_entry(self,detectionid, functiontype, objectid, filename, framecount, totalframes, classid, classname, coordinates, timestamp, jobid, sourceid, sub_sourceid):
	    try:
		    connection = psycopg2.connect(user="apex1", password="apex1", host="postgres", port="5432", database="viz")
		    cursor = connection.cursor() 
		    postgres_insert_query = """ INSERT INTO log VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""                                                
		    record_to_insert = (detectionid, functiontype, objectid, filename, framecount, totalframes, classid, classname, coordinates, timestamp, jobid , sourceid,  sub_sourceid, model_label_id)                                                                                                                                 
	    
		    cursor.execute(postgres_insert_query, record_to_insert)
		    connection.commit()   
            		  

		


	    except (Exception, psycopg2.Error) as error: 
		    print("Failed to insert record into table", error)

	    finally:
		# closing database connection.
    		if connection:
    		    cursor.close()
    		    connection.close()
    		    print("PostgreSQL connection is closed")


    def get_subbsource_name(self,sub_source_id):
        connection = psycopg2.connect(user="apex1", password="apex1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT sub_source_name FROM "sub_sources" WHERE sub_source_id={0}'.format(sub_source_id)
        cursor.execute(postgreSQL_select_Query)
        sub_source_name = cursor.fetchone()
        sub_source_name=sub_source_name[0]
        print(sub_source_name)
        return sub_source_name


    def get_source_name(self, source_id):
        connection = psycopg2.connect(user="apex1", password="apex1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT source_name FROM "Sources" WHERE source_id={0}'.format(source_id)
        cursor.execute(postgreSQL_select_Query)
        source_name = cursor.fetchone()
        source_name=source_name[0]
        print(source_name)
        return source_name


    def label_id(self, label_name):
        connection = psycopg2.connect(user="apex1", password="apex1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT label_id FROM "Model_labels" WHERE label_name={0}'.format(label_name)
        cursor.execute(postgreSQL_select_Query)
        label_id = cursor.fetchone()
        label_id=label_id[0]
        print(label_id)
        return label_id

#label_name=car                                                                                        
#Functionid=20211004115930
##Sourceid=20211005194713 
#sub_source_id=20211005062245
#cls=database_function()
#cls.get_label_name(Functionid)
#cls.get_function_type(Functionid)
#Sourceid=20210930053218
#cls.get_subbsource(Sourceid)
#sub_source_id=20210930053218
#cls.get_subbsource(Sourceid)
#cls.get_subbsource_name(sub_source_id)
#cls.get_source_name(Sourceid)
#cls.label_id(label_name)



