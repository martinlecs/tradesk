from orders import *

CLOSE_THRESHOLD = 2
PROJECTED_THRESHOLD = 5
SIZE = 100
STOP = 0
LIMIT = 0

class Trader:

    def __init__(self, api_con):
        self.api = api_con

    def decide(self, instrument, series):

        maxima = max(series)
        minima = min(series)
        peak_value = maxima if maxima > minima else minima
        projected = abs(series[0] - peak_value) / peak_value * 100

        open_orders = []

        if self.api.has_money:
            if peak_value == maxima and projected >= PROJECTED_THRESHOLD:
                # buy
                order = self.api.open_trade(instrument, SIZE, STOP, LIMIT)
                open_orders.append(Order(order, self.api.get_offer_snapshot()['buy']))
            else:
                # sell at market value
                self.api.sell_at_market_price(instrument, SIZE)

        if not self.api.get_open_positions().empty:
            df = self.api.get_open_positions()

            for _, row in df.iterrows():

                gain = (row['open'] - row['close']) / row['close'] * 100
                if row['is_Buy'] and gain >= CLOSE_THRESHOLD:
                    self.api.close_position(instrument, SIZE, STOP, LIMIT) #sell
                else:
                    self.api.close_position(instrument, SIZE, STOP, LIMIT) # buy

    def test_decide(self, series):
        maxima = max(series)
        minima = min(series)
        peak_value = maxima if maxima > minima else minima
        projected = abs(series[0] - peak_value) / peak_value * 100

        PHASE  = ""

        if self.api.has_money:
            if peak_value == maxima and projected >= PROJECTED_THRESHOLD:
                # buy
                PHASE = "open trade"
            else:
                # sell at market value
                PHASE = "sell at market"

        if self.api.get_open_positions().empty:
            # we got open positions
            df = self.api.get_open_positions()

            for _, row in df.iterrows():
                gain = (row['open'] - row['close']) / row['close'] * 100
                if row['is_Buy'] and gain >= CLOSE_THRESHOLD:
                    print("")
                else:
                    self.api.close_position(instrument, SIZE, STOP, LIMIT) # buy

        return PHASE

    def printSeries(self, series):
        print(series)