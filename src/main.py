# from src.auxilliaries import *
# import tensorflow as tf
from src.tradingapi import TradingAPI
from src.trader import Trader
import os
import time

TRADING_INTERVAL = 5

if __name__ == "__main__":

    api = TradingAPI()

    # data = api.get_historical_data('EUR/USD', period='m1', number=10000)
    # print(data)
    #
    # data = api.get_instruments()
    #
    # print(data)

    tr = Trader(api)

    series = [1.2, 1.3, 1.4, 1.5, 1.6]

    tr.printSeries(series)
    tr.decide(series)



    #
    # # We work with the average of the highs and low of the stock price.
    # mids = get_mid_prices(data)
    #
    # # Split into training and testing. About 90 and 10% used for the former and latter respectively
    # training, testing = split_data(mids)
    #
    # # Scale data to the range [0,1] due to varying magnitude fluctuations of the stock as a function of time.
    # training, testing = scale_data(training, testing)
    #
    # # Smooth the data in order to rid ourselves of the inherent raggedness associated with variations in stock
    # # prices. For obvious reasons this is only performed upon the training data
    # training = exponential_smoothing(training)
    #
    # mid_stock_prices = gather_data(training, testing)
    #
    # # TODO: Plot training data after smoothing and rescaling (Include image in final presentation perhaps)
    #
    # # If the directory exists then this means a model exists. We proceed with making real-time financial predictions
    # # and trading based on these predictions
    # if model_directory_path + '.meta' not in os.listdir(path='./'):
    #
    #     # In the instance previous sessions were run the graph needs to be reset
    #     tf.reset_default_graph()
    #
    #     predictions, testing_losses, x_axis_values = machine_learn(training, mid_stock_prices)
    #
    #     save_data(predictions, testing_losses, x_axis_values)
    #
    # else:
    #
    # tr = Trader(api)
    # api.subscribe("EUR/USD")
    # time.sleep(TRADING_INTERVAL)
    #
    # while True:
    #     live_stream_data = api.get_live_data("EUR/USD", 100)
    #     #predictions = get_predictions(testing[:sequence_size])
    #
    #     tr.decide(predictions)
    #
    #     #send data to SSH
    #
    #     print(live_stream_data)
    #     time.sleep(TRADING_INTERVAL)

    api.shutdown()


        # TODO: The predictions in the csv file could be picked up by Splunk. A live demonstration of this during
        # TODO: the presentation would be ideal


