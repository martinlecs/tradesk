class Order:

    def __init__(self, order_id, aim):
        self.order_id = order_id
        self.aim_price = aim

    def get_aim_price(self):
        return self.aim_price

    def get_order_id(self):
        return self.get_order_id()