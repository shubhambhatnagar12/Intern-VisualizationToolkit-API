from fastapi import FastAPI,File,UploadFile,Form
import json
#import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import StringIO 
from monthly_sales22 import func
from stock_time_series import funcStock
#import boto3

#from fastapi.middleware.cors import CORSMiddleware


origins = ['*']
     #"http://localhost",
     #"http://localhost:8000"
     #"http://localhost:8080",
 
app=FastAPI()
# # This completely screws up CORS and is highly insecure but excellent for prototyping
app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
 )



@app.get("/")
async def helloworld():
    return "hello from the api"
#=====================================================================================================================================
#this route takes input from User in the form of File and process that file and returns results to frontend
@app.post("/Receive_File_From_User_Financials")
async def submitFile(userInput:str=Form(...),upfiles: list[UploadFile] = File(...)):
    def upload_file_to_df(byte_stream):
        ENCODING = 'utf-8'
        return pd.read_csv(StringIO(str(byte_stream, ENCODING)), encoding=ENCODING)
    #creating dataframes
    df_from_each_file =  [upload_file_to_df(byte_stream) async for byte_stream in (await f.read() for f in upfiles)]

    df =pd.concat(df_from_each_file, ignore_index=True)

    return func(df)
#-==================================================================================================================================
#this route takes stock related data and returs json format
@app.post("/Receive_File_From_User_Stocks")
async def submitFile(userInput:str=Form(...),upfiles: list[UploadFile] = File(...)):
    
    #function for converting byte stream to string
    def upload_file_to_df(byte_stream):
        ENCODING = 'utf-8'
        return pd.read_csv(StringIO(str(byte_stream, ENCODING)), encoding=ENCODING)
    #creating dataframes
    df_from_each_file =  [upload_file_to_df(byte_stream) async for byte_stream in (await f.read() for f in upfiles)]
    
    df =pd.concat(df_from_each_file, ignore_index=True)
    
    return funcStock(df)
#=============================================================================================================================================
#this route is for Umap_minst data and use its data to plot scatter plot
# @app.post("/Scatter_Plot")
# async def sctterplot():
#     data = fetch_openml("mnist_784", version=1)
#     report=umapData(data)
#     return report


# ==========================================================================================================================================
# @app.post("/Receive_Data_Fr_MySQLDB")
# async def setupConnection(host:str=Form(...),user:str=Form(...),passwd:str=Form(...),database:str=Form(...)):
#     mydb=mysql.connector.connect(host=host,user=user,passwd=passwd,database=database,auth_plugin='mysql_native_password')
#     mycursor=mydb.cursor()
#     mycursor.execute("show databases")
#     for db in mycursor :
#         print(db)
