from fastapi import FastAPI,File,UploadFile,Form
#from fastapi.responses import FileResponse
#import mysql.connector
import pandas as pd
from io import StringIO 
from monthly_sales2 import func
from stock_time_series import funcStock
app=FastAPI()


@app.get("/")
async def helloworld():
    return "hello from the api"


#this route takes input from User in the form of File and process that file and returns results to frontend
@app.post("/Receive_File_From_User_Financials")
async def submitFile(userInput:str=Form(...),upfiles: list[UploadFile] = File(...)):
    #print(userInput)
    #printing name of files
    #for file in upfiles:
       # print(file.filename)
    #function for converting byte stream to string
    def upload_file_to_df(byte_stream):
        ENCODING = 'utf-8'
        return pd.read_csv(StringIO(str(byte_stream, ENCODING)), encoding=ENCODING)
    #creating dataframes
    df_from_each_file =  [upload_file_to_df(byte_stream) async for byte_stream in (await f.read() for f in upfiles)]
    #print(type(df_from_each_file))
    #print(df_from_each_file)
    df =pd.concat(df_from_each_file, ignore_index=True)
    #Send this file object for processing
    #Receive output and send this as response
    return func(df)

#this route takes stock related data and returs json format
@app.post("/Receive_File_From_User_Stocks")
async def submitFile(userInput:str=Form(...),upfiles: list[UploadFile] = File(...)):
    #print(userInput)
    #printing name of files
    #for file in upfiles:
        #print(file.filename)
    #function for converting byte stream to string
    def upload_file_to_df(byte_stream):
        ENCODING = 'utf-8'
        return pd.read_csv(StringIO(str(byte_stream, ENCODING)), encoding=ENCODING)
    #creating dataframes
    df_from_each_file =  [upload_file_to_df(byte_stream) async for byte_stream in (await f.read() for f in upfiles)]
    #print(type(df_from_each_file))
    #print(df_from_each_file)
    df =pd.concat(df_from_each_file, ignore_index=True)
    #Send this file object for processing
    #Receive output and send this as response
    return funcStock(df)


#@app.post("/Receive_Data_Fr_MySQLDB")
#async def setupConnection(host:str=Form(...),user:str=Form(...),passwd:str=Form(...),database:str=Form(...)):
    #mydb=mysql.connector.connect(host=host,user=user,passwd=passwd,database=database,auth_plugin='mysql_native_password')
    #mycursor=mydb.cursor()
    #mycursor.execute("show databases")
    #for db in mycursor :
        #print(db)

