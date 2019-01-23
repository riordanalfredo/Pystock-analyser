import numpy as np
from datetime import datetime
from selenium import webdriver
import os

#For Prediction
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split

#For Stock Data
from iexfinance.stocks import get_historical_data


def get_stocks(n):
    # Navigating to the Yahoo stock screener
    driver = webdriver.Chrome('C:/Users/riord/Documents/GitHub/Pystock-analyser/chromedriver.exe')
    url = "https://finance.yahoo.com/screener/predefined/aggressive_small_caps?offset=0&count=202"
    driver.get(url)

    stock_list = []
    n += 1
    for i in range(1,n):
        ticker = driver.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr[' + str(i) + ']/td[1]/a')
        stock_list.append(ticker.text)
    driver.quit()

    for i in stock_list:
        predict_data(i,5)


def predict_data(stock,days):
    start = datetime(2017, 1, 1)
    end = datetime.now()

    df = get_historical_data(stock, start=start, end=end, output_format='pandas')
    if os.path.exists('./Exports'):
        csv_name = ('Exports/' + stock + '_Export.csv')
    else:
        os.mkdir("Exports")
        csv_name = ('Exports/' + stock + '_Export.csv')
    df.to_csv(csv_name)
    df['prediction'] = df['close'].shift(-1)
    df.dropna(inplace=True)

    forecast_time = int(days)

    # numpy graph creation
    X = np.array(df.drop(['prediction'], 1))
    Y = np.array(df['prediction'])
    X = preprocessing.scale(X)
    X_prediction = X[-forecast_time:]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5)

    # Perform Regression on the training data
    clf = LinearRegression()
    clf.fit(X_train, Y_train)
    prediction = (clf.predict(X_prediction))

    # Sending the SMS if the predicted price of the stock is at least 1
    # greater than the previous closing price
    last_row = df.tail(1)

    if float(prediction[4]) > (float(last_row['close'])):
        output = ("\n\nStock: " + str(stock) + "\nPrior Close:\n"
                  + str(last_row['close']) + "\n\nPrediction in 1 Day: "
                  + str(prediction[0]) + "\nPrediction in 5 Days: "
                  + str(prediction[4]))
        print("Output: " + output)


if __name__ == "__main__":
    predict_data('AAPL',40)
    # get_stocks(200)
