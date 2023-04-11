import sqlite3
from sqlite3 import Error
from cds_py_logger import LOGGER,logger
from enum import Enum


class DataBase():
    def __init__(self,path="database/viaphoton.db"):
        self.logger = LOGGER(Logger_Name="SeederApp",Debug=False)
        self.DataBasePath = path
        self._conn = self.CreateConnection()
        self.DbCursor = self._conn.cursor()
        

    def Close(self, commit=True):
        if commit:
            self._conn.commit()
        self._conn.close()
        self.logger.LOG_INFO("Database closed")
    def CreateConnection(self):
        """create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.DataBasePath, check_same_thread=False)
            self.logger.LOG_INFO("Database Connection created")
            return conn
        except Error as e:
            self.logger.LOG_ERROR(f"DB Error {e}")
        return conn
    def CreateTable(self, table):
        """create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            self.DbCursor.execute(table)
            self._conn.commit()
        except Error as e:
            self.logger.LOG_ERROR(f"DB Error {e}")
            
    def ExecuteQuery(self,Query,Params=None):
        try:
            if self._conn:
                if Params:
                    self.DbCursor.execute(Query, Params)
                else:
                    self.DbCursor.execute(Query)
                self._conn.commit()
            else:
                self.logger.LOG_WARN(f"Databse connection not open")        
        except Exception as err:
            self.Close()
            self.logger.LOG_WARN(f"Error Exceuting Query.Err:{err}")        
class UserDataBaseSeeder(DataBase):
    class UserDatabaseIndex (Enum):
        UserIdIndex = 0
        UserNameIndex = 1
        UserUidIndex = 2
    def __init__(self,DatabasePath="database/",DatabaseName="viaphoton.db",RunningEnviroment="STAGE"):
        self.DatabasePath = DatabasePath
        self.DatabaseName = DatabasePath+DatabaseName
        DataBase.__init__(self,self.DatabaseName)
        self.RunEnv = RunningEnviroment
        UserDataTableQuery = """CREATE TABLE IF NOT EXISTS {}_Users (
                            id integer PRIMARY KEY,
                            Name TEXT NOT NULL,
                            UID TEXT NOT NULL
                            );""".format(self.RunEnv)
        self.logger.LOG_INFO("Initialize UserDataBaseSeeder: {}".format(self.DatabaseName))  # get current directory
        self.CreateTable(UserDataTableQuery)

    def InsertUserData(self,UserData):
        UserDataInsertWithParam = """INSERT or REPLACE  INTO {}_Users(Name, id, UID)  
                          VALUES (?,?,?);""".format(self.RunEnv)
        self.ExecuteQuery(UserDataInsertWithParam,UserData)
        self.logger.LOG_INFO("User data inserted: {}".format(UserData))
    def getUserData(self):
        data= None
        GetUserDataQuery = """SELECT * from {}_Users""".format(self.RunEnv)
        self.ExecuteQuery(GetUserDataQuery)
        try:
            result = self.DbCursor.fetchall()
            if result:
                self.logger.LOG_INFO("User ID from database: {}".format(result))
            return result

        except Exception as e:
            self.logger.LOG_INFO("User ID not found in database,Err: {}".format(e) )
            return None
    
    def SeedUserData(self,UserDataList):
        for items in UserDataList:
            self.InsertUserData((items[self.UserDatabaseIndex.UserIdIndex.value],items[self.UserDatabaseIndex.UserNameIndex.value],items[self.UserDatabaseIndex.UserUidIndex.value]))
    
if __name__ == "__main__":
    logger.LOG_INFO("Init main")
    InitialSeedData = [('Guest User', 2032, '0000000000'), ('Guest User 1', 1901, '0005482088'),
                       ('Guest User 2', 1902, '0000658413'), ('Guest User 3', 1903, '0005537950'),
                       ('Guest User 4', 1904, '0000548732'), ('Guest User 5', 2886, '0004760468'),
                       ('Guest User 6', 2888, '0001691236'), ('Guest User 7', 2889, '0001733921'),
                       ('Leslie Montejano', 3381, '2150883352'), ('John Guzman', 1936, '0012056321'),
                       ('Cathy Rodriguez', 1934, '0012056310'), ('James Milder', 1072, '0005832722'), 
                       ('Morgan Dunn', 331, '0008285793'), ('Glen Williams', 643, '0008416954'),
                       ('Felix Feral', 644, '0012056369')]
    DbHandle = UserDataBaseSeeder(DatabasePath="")
    DbHandle.SeedUserData(InitialSeedData)