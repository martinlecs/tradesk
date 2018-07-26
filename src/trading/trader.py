CLOSE_THRESHOLD = 2
PROJECTED_THRESHOLD = 5
SIZE = 1
STOP = None
LIMIT = 20

class Trader:

    def __init__(self, api_con):
        self.api = api_con

    def decide(self, instrument, series, trade=True):

        maxima = max(series)
        minima = min(series)
        peak_value = maxima if maxima > minima else minima
        projected = abs(series[0] - peak_value) / peak_value * 100

        PHASE  = ""

        if not trade: #self.api.get_open_positions():
            if peak_value == maxima and projected >= PROJECTED_THRESHOLD:
                # buy
                self.api.open_trade(instrument, SIZE, STOP, LIMIT)
                PHASE = "buy"
            else:
                # sell at market value
                self.api.sell_at_market_price(instrument, SIZE)
                PHASE = "sell"
        else:
            # we got open positions
            df = self.api.get_open_positions()
            for _, row in df.iterrows():
                gain = (row['open'] - row['close']) / row['close'] * 100
                if row['is_Buy'] and gain >= CLOSE_THRESHOLD:
                    self.api.close_position(instrument, SIZE, STOP, LIMIT) #sell
                else:
                    self.api.close_position(instrument, SIZE, STOP, LIMIT) # buy

        return PHASE


    def printSeries(self, series):
        print(series)