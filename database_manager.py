import psycopg2
import logging
import os

class DatabaseManager:

    def __init__(self,database_url):
        self.database_url=database_url

    

    
    def check_table_exists(self)->bool:
        table_list = ["offers","leads","scores"]
        conn = None
        cursor = None
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            for table_name in table_list:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s
                    );
                """, (table_name,))
                exists = cursor.fetchone()[0]
                if not exists:
                    return False
            return True
        
        except Exception as e:
            logging.error(f"exception occured in checking database schema : {e}")
            raise
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()


    def create_schema(self):
        folder_path="dbscripts"
        conn = None
        cursor = None
        try:
            conn=psycopg2.connect(self.database_url)
            cursor=conn.cursor()
            for filename in os.listdir(folder_path):
                file_path=os.path.join(folder_path,filename)
                if os.path.isfile(file_path):
                    with open(file_path,'r',encoding='utf-8') as f:
                        content=f.read()
                        commands = [cmd.strip() for cmd in content.split(';') if cmd.strip()]
                        for ddl_command in commands:
                            cursor.execute(ddl_command)
                else:
                    logging.error("sql file format not correct")
            conn.commit()
        
        except Exception as e:
            logging.error(f"error in creating database schema : {e}")
            raise

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()



    def initialize_database(self):
        if not self.check_table_exists():
            self.create_schema()
        logging.info("database schema ready")



    