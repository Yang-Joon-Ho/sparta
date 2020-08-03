import zipline
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime

from zipline.api import order, symbol

start = datetime.datetime(2010,1,1)
end = datetime.datetime(2016,3,19)

data = web.DataReader("AAPL", "yahoo", start, end)
plt.plot(data.index, data['Adj Close'])

def handle_data(context, data) :
    order(symbol('AAPL'), 1)

data.head()