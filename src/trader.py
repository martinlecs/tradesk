from src.tradingapi import *

CLOSE_THRESHOLD = 10
PROJECTED_THRESHOLD = 5

class Trader:

    def __init__(self, api_con):
        self.api = api_con

    #TODO: Implement decision making here
    def decide(self, series, trade=False):

        #assume list of floats [1.2, 1.3,1.3]
        maxima = max(series)
        minima = min(series)
        peak_value = maxima if maxima > minima else minima
        print(peak_value)

        projected = abs(series[0] - peak_value) / peak_value * 100

        PHASE  = ""

        if not trade: #self.api.get_open_positions():
            if peak_value == maxima and projected >= PROJECTED_THRESHOLD:
                # buy
                #self.api.open_trade()
                PHASE = "buy"
                print("buy")
            else:
                # sell at market value
                #self.api.sell_at_market_price()
                PHASE = "sell"
                print("sell")
        # else:
        #     # we got open positions
        #     trade = self.api.get_open_positions()
        #     if trade['S/B'] is 'B' and trade['asset_price'] >= CLOSE_THRESHOLD:
        #         self.api.close_position() #sell
        #     else:
        #         # sell
        #         self.api.close_position() # buy

        return PHASE


    def printSeries(self, series):
        print(series)