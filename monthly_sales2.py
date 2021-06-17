import json
import pandas as pd
import numpy as np
import glob
import os
import random


def func(df):

    df = df.dropna(how='any')


    df = df[df['Order Date'].str[0:2] != 'Or']
    df.head()

    df['Month'] = df['Order Date'].str[0:2]
    df['Month'] = df['Month'].astype('int32')
    df.head()
    df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'])
    df['Price Each'] = pd.to_numeric(df['Price Each'])
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df.head()

    df['Hour'] = df['Order Date'].dt.hour
    df.head()
    def get_city(address):
        return address.split(',')[1]
    def get_state(address):
        return address.split(',')[2].split(' ')[1]

    df['City'] = df['Purchase Address'].apply(lambda x:get_city(x)+' ('+get_state(x)+')')
    df.head()
    df['Sales'] = df['Quantity Ordered']*df['Price Each']
    df.head()
    #1
    bymonth = df.groupby('Month').sum()
    df['Hour'] = df['Order Date'].dt.hour
    #2
    hours = [hour for hour, df in df.groupby('Hour')]
    hours_df=df.groupby(['Hour']).count()

    df['Minute'] = df['Order Date'].dt.hour
    citysales =df[['City','Sales']]
    #3
    results = df.groupby('City').sum()
    cities = [city for city, df in df.groupby('City')]
    #4
    product_group = df.groupby('Product')

    quantity_ordered = product_group.sum()['Quantity Ordered']
    products = [p for p, df in product_group]
    prices = df.groupby('Product').mean()['Price Each']
    jenc = json.JSONEncoder()


    return jenc.encode({
        "name" : 'monthly sales report',
        "id"   : random.randint(0, 2 ** 64 - 1),
        "results" : {
            "monthy sales" : bymonth.to_json(),
            "hours sales" : hours_df.to_json(),
            "city sales" : results.to_json(),
            
        }
    }) 







if __name__ == '__main__':
    # Frontend code. These will be the input we get from the frontend like a file or DB connection. Specifying directly for simplicity
    path = os.curdir                     # use your path
    all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent

    df_from_each_file = (pd.read_csv(f) for f in all_files)
    df   = pd.concat(df_from_each_file, ignore_index=True)

    # Here, we are supposed to push these inputs to the API
    # This is where report is generated. As this interaction can't take place directly in production we will be using an API as an intermediator. The API will do things like store reports, update report status to users, logging, compute billing related information by tracking usage
    report = func(df)
    # Here, the frontend is supposed to retrieve the report
    # This is frontend code again. Where the results are displayed to the user. I am simply printing here but in practice visualizations will be made here, also other insights will be displayed here.
    print(report)    
