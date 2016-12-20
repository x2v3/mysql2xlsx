import pymysql

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

    def get_query_table(self,name,sql,*params):
        conn=self.get_connection()
        cursor=conn.cursor()
        cursor.execute(sql,params)
        cursor.close()
        table=Datatable()
        table.name=name
        table.query_sql=sql
        table.query_params=params
        table.database=self
        return table


class Datatable:
    name=''
    columns=None
    rows=None
    database=None
    query_sql=None
    query_params=None

    def __init__(self,name=None,query=None):
        if name is not None:
            self.name=name
        if query is not None:
            self.query_sql=query

    def get_columns(self):        
        if self.columns is None:
            self.query_table_info()
        return self.columns

    def get_rows(self):
        if self.rows is None:
            self.query_table_info()
        return self.rows

    def query_table_info(self):
        sql='select * from `%s`'%self.name
        if self.query_sql is not None:
            sql=self.query_sql
        cursor=self.database.get_connection().cursor()
        cursor.execute(sql,self.query_params)
        rs=cursor.fetchall()
        self.columns=[c[0] for c in cursor.description]
        self.rows=rs
        cursor.close()



