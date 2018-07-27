import random

CLOSE_THRESHOLD = 0.02  # 2%
PROJECTED_THRESHOLD = 5
SIZE = 100
STOP = 10
LIMIT = 0

class Trader:

    def __init__(self, api_con):
        self.api = api_con

    def decide(self, instrument, series):

        maxima = max(series)
        minima = min(series)
        peak_value = maxima if maxima > minima else minima
        projected = abs(series[0] - peak_value) / peak_value * 100

        open_orders = {}

        if self.api.has_money:
            if peak_value == maxima and projected >= PROJECTED_THRESHOLD:
                # buy
                order = self.api.open_trade(instrument, SIZE, -STOP, True)
                open_orders[order] = projected
            else:
                # sell at market value
                self.api.open_trade(instrument, SIZE, STOP, False)

        if not self.api.get_open_positions().empty:
            df = self.api.get_open_positions()

            for _, row in df.iterrows():
                if row['is_Buy'] and self.isAcceptableBuy(self.api.get_orders_snapshot()['buy'], open_orders[row['tradeId']]):
                    self.api.close_trade(row['tradeId'], row['amountK'])

    def isAcceptableBuy(self, current_price, projected_price):
        return True if (abs(projected_price - current_price) / projected_price) > CLOSE_THRESHOLD else False

    def printSeries(self, series):
        print(series)


def random_floats(low, high, size):
    return [random.uniform(low, high) for _ in range(size)]
