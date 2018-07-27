from auxilliaries import *
import tensorflow as tf
from tradingapi import TradingAPI
from trader import Trader
import os
import time

TRADING_INTERVAL = 5


if __name__ == "__main__":

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(server, port, username, password)

    # index = create_client()

    api = TradingAPI()
    tr = Trader(api)

    while True:

        data = api.get_historical_data('EUR/USD', 'm5', 10000)

        # We work with the average of the highs and low of the stock price.
        mids = get_mid_prices(data)

        # Split into training and testing. About 90 and 10% used for the former and latter respectively
        training, testing = split_data(mids)

        # Scale data to the range [0,1] due to varying magnitude fluctuations of the stock as a function of time.
        training, testing = scale_data(training, testing)

        # Smooth the data in order to rid ourselves of the inherent raggedness associated with variations in stock
        # prices. For obvious reasons this is only performed upon the training data
        training = exponential_smoothing(training)

        mid_stock_prices = gather_data(training, testing)

        # TODO: Plot training data after smoothing and rescaling (Include image in final presentation perhaps)
        # If the directory exists then this means a model exists. We proceed with making real-time financial predictions
        # and trading based on these predictions
        # In the instance previous sessions were run the graph needs to be reset
        tf.reset_default_graph()

        start_time = time.time()

        predictions, testing_losses, x_axis_values = machine_learn(training, mid_stock_prices)

        finish_time = time.time()

        print (finish_time - start_time)

        time.sleep(120 - (finish_time - start_time))

        previous_data = get_mid_prices((api.get_historical_data('EUR/USD', 'm5', number=sequence_size)))
        preds = (get_predictions(previous_data))

        # tr.decide('EUR/USD', preds)

        output_to_csv(preds, time.time())
        api.batch_generate_csv()

        sending_directory = os.listdir(csv_directory)

        # scp bash function in python
        with SCPClient(ssh.get_transport()) as scp:
        	for file in range(len(sending_directory)):
        		scp.put(str(csv_directory + sending_directory[file]), put_address)
        print ('CSV HAS SENT YO!!!!')

        # save_data(predictions, testing_losses, x_axis_values)

