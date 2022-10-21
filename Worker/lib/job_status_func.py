import psycopg2

class status_update:
    def job_status(self, status, job_id):
        
        sql = """ UPDATE public."Jobs"
                  SET status = %s
                  WHERE job_id = %s"""
        conn = None
    
        try:
            connection = psycopg2.connect(user="apexroot1", password="apexroot1", host="postgres", port="5432", database="viz")
            cursor = connection.cursor() 
            
            sql = """ UPDATE public."Jobs"
                      SET status = %s
                      WHERE job_id = %s"""
            
            cursor.execute(sql, (status, job_id))
            updated_rows = cursor.rowcount
            connection.commit()
            cursor.close()
    
    
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                
#clss=status_update()
#status = "finn"
#job_id= 20211012142935
#clss.job_status(job_id, status)


