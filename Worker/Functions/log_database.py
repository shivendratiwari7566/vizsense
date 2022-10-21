import psycopg2      
import json                                                                                                                                     

class database_function:

    def get_model_id_from_lto(self,Functionid):
        try:
            connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
            cursor = connection.cursor() 
            #postgreSQL_select_Query = 'SELECT * FROM public."Jobs";'            
            print(Functionid)
            postgreSQL_select_Query = 'SELECT label_id FROM public."Function_lto" WHERE function_id={0}'.format(Functionid)  
            cursor.execute(postgreSQL_select_Query) 
            label_id = cursor.fetchone() 
            label_id=label_id[0]
            print(label_id)

            postgreSQL_select_Query = 'SELECT model_id FROM public."Model_labels" WHERE label_id={0}'.format(label_id)  
            cursor.execute(postgreSQL_select_Query) 
            model_id = cursor.fetchone() 
            model_id=model_id[0]
            print(model_id)


            return model_id
  
        except (Exception, psycopg2.Error) as error: 
            print("Failed", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    
 



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

    def get_model_specname(self, model_id):
        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT model_specname FROM "Models" WHERE model_id={0}'.format(model_id)
        cursor.execute(postgreSQL_select_Query)
        model_specname = cursor.fetchone()
        model_specname=model_specname[0]
        print(model_specname)
        return model_specname

    def get_model_signature(self, model_id):
        connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT model_signature FROM "Models" WHERE model_id={0}'.format(model_id)
        cursor.execute(postgreSQL_select_Query)
        model_signature = cursor.fetchone()
        model_signature=model_signature[0]
        print(model_signature)
        return model_signature





#label_name="'car'"                                                                                        
#Functionid=20211026075201 
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
                                                                                          
#cls=database_function()

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

#function_id=20211028070659
#cls.get_model_id_from_lto(function_id)


#model_id=20210930051819
#model_label_id=2
#model_label_id=3
#model_id=20211126143408
#cls.get_label_name(model_label_id, model_id)
