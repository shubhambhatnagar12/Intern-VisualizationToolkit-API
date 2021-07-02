import glob
import random
import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime  # To access datetime
from pandas import Series
import json
import os



def funcStock(df):
    # df = df.dropna(how='any')

    # df.head()
    # df.describe()
    # df = df[df['Date']]
    df['Date'] = pd.to_datetime(df['Date'])
    df.head()

    # 1
    df1_volume = [i for i in df.Volume]
    df1_volume = json.dumps(df1_volume)
    df1_Close = [i for i in df.Close]
    df1_Close = json.dumps(df1_Close)

    # 2
    min_volume = int(df.Volume.min())
    min_volume = json.dumps(min_volume)
    # print(min_volume)
    max_volume = int(df.Volume.max())
    max_volume = json.dumps(max_volume)
    # print(max_volume)

    df1 = df[['Date', 'VWAP']]
    df1['Date'] = pd.to_datetime(df1['Date'])
    df1['year'] = df1.Date.dt.year
    df1['month'] = df1.Date.dt.month
    df1['day'] = df1.Date.dt.day
    df1['day of week'] = df1.Date.dt.dayofweek

    # Set Date column as the index column.
    df1.set_index('Date', inplace=True)
    df1.head()

    # 3
    df1_VWAP = [i for i in df['VWAP']]
    df1_VWAP = json.dumps(df1_VWAP)
    df1_VWAP_mean_yearwise = [i for i in df1.groupby('year')['VWAP'].mean()]
    df1_VWAP_mean_yearwise = json.dumps(df1_VWAP_mean_yearwise)
    df1_VWAP_mean_weekwise = [i for i in df1.groupby('day of week')['VWAP'].mean()]
    df1_VWAP_mean_weekwise = json.dumps(df1_VWAP_mean_weekwise)
    max_VWAP_at_the_endofyear = df1['VWAP'].resample('A').mean().max()
    max_VWAP_at_the_endofyear = json.dumps(max_VWAP_at_the_endofyear)
    max_VWAP_at_the_startofyear = df1['VWAP'].resample('AS').mean().max()
    max_VWAP_at_the_startofyear = json.dumps(max_VWAP_at_the_startofyear)

    # 5
    # df1_VWAP
    df1_VWAP_mean_rollingwindow = [i for i in df1.rolling(window=30).mean()['VWAP']]
    df1_VWAP_mean_rollingwindow = json.dumps(df1_VWAP_mean_rollingwindow)

    #jenc = json.JSONEncoder()
    # space = int('      '*5)
    return ({
        "name": "Stock Market time series",
        "id": random.randint(0, 2 ** 64 - 1),
        "results": {
            "Volume": df1_volume,
            "Close": df1_Close,
            "min_volume": min_volume,
            "max_volume": max_volume,
            "VWAP": df1_VWAP,
            "VWAP yearwise": df1_VWAP_mean_yearwise,
            "VWAP weekwise": df1_VWAP_mean_weekwise,
            "Max VWAP End of year": max_VWAP_at_the_endofyear,
            "Max VWAP start of year": max_VWAP_at_the_startofyear,
            "Rolling window VWAP": df1_VWAP_mean_rollingwindow,

        }
    })
    # 6  Prediction
    # new_dataset = pd.DataFrame(index=range(0, len(df)), columns=['Date', 'Close'])
    # for i in range(0, len(data)):
    #     new_dataset["Date"][i] = data['Date'][i]
    # new_dataset["Close"][i] = data["Close"][i]
    # scaler = MinMaxScaler(feature_range=(0, 1))
    # final_dataset = new_dataset.values
    # train_data = final_dataset[0:987, :]
    # valid_data = final_dataset[987:, :]
    # scaler = MinMaxScaler(feature_range=(0, 1))
    # scaled_data = scaler.fit_transform(final_dataset)
    # x_train_data, y_train_data = [], []
    # for i in range(60, len(train_data)):
    #     x_train_data.append(scaled_data[i - 60:i, 0])
    # y_train_data.append(scaled_data[i, 0])
    #
    # x_train_data, y_train_data = np.array(x_train_data), np.array(y_train_data)
    # x_train_data = np.reshape(x_train_data, (x_train_data.shape[0], x_train_data.shape[1], 1))
    # lstm_model = Sequential()
    # lstm_model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train_data.shape[1], 1)))
    # lstm_model.add(LSTM(units=50))
    # lstm_model.add(Dense(1))
    # inputs_data = new_dataset[len(new_dataset) - len(valid_data) - 60:].values
    # inputs_data = inputs_data.reshape(-1, 1)
    # inputs_data = scaler.transform(inputs_data)
    # lstm_model.compile(loss='mean_squared_error', optimizer='adam')
    # lstm_model.fit(x_train_data, y_train_data, epochs=1, batch_size=1, verbose=2)
    # X_test = []
    # for i in range(60, inputs_data.shape[0]):
    #     X_test.append(inputs_data[i - 60:i, 0])
    # X_test = np.array(X_test)
    # X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    # predicted_closing_price = lstm_model.predict(X_test)
    # predicted_closing_price = scaler.inverse_transform(predicted_closing_price)
    # train_data = new_dataset[:987]
    # valid_data = new_dataset[987:]
    # valid_data['Predictions'] = predicted_closing_price
    # df1_Close
    # df1_prediction = [i for i in (valid_data[['Close', "Predictions"]])


