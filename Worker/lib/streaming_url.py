import socket   
import psycopg2

class  stream_url:

    def create_and_store(self,jobid,sub_source_id):
    
        try:
            connection = psycopg2.connect(user="apex1", password="apex1", host="postgres", port="5432", database="viz")
            cursor = connection.cursor() 
            hostname = socket.gethostname()  
            print("hostname", hostname)  
            jobid=jobid
            #IPAddr = socket.gethostbyname(hostname)    
            #print("Your Computer IP Address is:" + IPAddr) 
            sub_source_id=str(sub_source_id)
            #port=str(port_number)
            port=sub_source_id[-2:]
            #sub_source_id=int(sub_source_id)
            print(port)
            url="tcp://"+str(hostname)+":55"+port
            url=str(url)
            print(url)
            status="running"
            postgres_insert_query = """ INSERT INTO streaming_url VALUES (%s, %s, %s, %s)"""                                                
            record_to_insert = (jobid, sub_source_id, url, status)
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()   

        
        except (Exception, psycopg2.Error) as error: 
            print("Failed", error)
        
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                
                
                
    def get_url(self,sub_source_id):
    
        try:
            connection = psycopg2.connect(user="apex1", password="apex1", host="postgres", port="5432", database="viz")
            cursor = connection.cursor() 
            postgreSQL_select_Query = 'SELECT url FROM public."streaming_url" WHERE sub_source_id={0}'.format(sub_source_id) 
            cursor.execute(postgreSQL_select_Query) 
            url = cursor.fetchone()
            url=url[0]
            print(url)
            return url

        
        except (Exception, psycopg2.Error) as error: 
            print("Failed", error)
        
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


jobid=20211011181636
sub_source_id=20211005194714
port_number=5553
cls=stream_url()
cls.create_and_store(jobid,sub_source_id)
#cls.get_url(sub_source_id)

