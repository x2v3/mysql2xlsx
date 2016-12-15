import pymysql
import logging

class Database:
    mysql_server='localhost'
    mysql_user='root'
    mysql_pwd=None
    mysql_port=3306
    mysql_db_name='mysql'
    db_connection=None

    logger=None

    datatables=None
    
    def __init__(self):
        #self.logger=logging.getLogger('databaseLog')
        pass

    def get_tables(self):
        #self.logger.info('in get_tables')
        if self.datatables is None:
            conn = self.get_connection()
            cursor=conn.cursor()
            sql='show tables;'
            cursor.execute(sql)
            rs=cursor.fetchall()
            self.datatables=[]

            for t in rs:
                table=Datatable()
                table.name=t[0]
                table.database=self
                self.datatables.append(table)
        return self.datatables;
        

    def get_connection(self):
        if self.db_connection is None:
            self.db_connection=pymysql.connect(host=self.mysql_server,user=self.mysql_user,password=self.mysql_pwd,db=self.mysql_db_name)
        return self.db_connection


class Datatable:
    name=''
    columns=None
    rows=None
    database=None

    def get_columns(self):
        if self.columns is None:
            sql='select * from %s'%self.name
            self.query_table_info(sql)
        return self.columns

    def get_rows(self):
        if self.rows is None:
            sql='select * from %s'%self.name
            self.query_table_info(sql)
        return self.rows

    def query_table_info(self,sql,*args):
        cursor=self.database.get_connection().cursor()
        cursor.execute(sql,args)
        rs=cursor.fetchall()
        self.columns=[c[0] for c in cursor.description]
        self.rows=rs
        cursor.close()



