from itertools import product

from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import math as Math

class Trader:

    def __init__(self):
        self.LIMIT_QTY = 80
        self.START_PRICE = None
        self.ORDER_SIZE = 13
        self.ROOT_SLOPE = 0.001
        self.MAX_VARIANCE = 28
        self.WINDOW_SIZE = 100
        self.prices = []

    def bid(self, price, qty):
        return 15

    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            current_position = state.position.get(product, 0)
            buy_orders = order_depth.buy_orders
            sell_orders = order_depth.sell_orders


            '''
            if product == "INTARIAN_PEPPER_ROOT" and buy_orders and sell_orders:
                current_position = state.position.get(product, 0)
                remaining_capacity = self.LIMIT_QTY - current_position

                for ask_price, ask_qty in sorted(order_depth.sell_orders.items()):
                    if remaining_capacity <= 0: break

                    available_qty = -ask_qty
                    trade_qty = min(available_qty, remaining_capacity)
                    trade_qty = min(trade_qty, self.ORDER_SIZE)

                    if trade_qty > 0 and ask_price % 1000 > 990 or ask_price % 1000 < 10:
                        orders.append(Order(product, ask_price, trade_qty))
                        remaining_capacity -= trade_qty
            '''
            
            if product == "INTARIAN_PEPPER_ROOT" and buy_orders and sell_orders:
                current_position = state.position.get(product, 0)

                if self.START_PRICE is None:
                    self.START_PRICE = (max(buy_orders) + min(sell_orders)) / 2
                
                best_bid = max(buy_orders)
                best_ask = min(sell_orders)
                mid_price = (best_bid + best_ask) / 2

                self.prices.append(mid_price)
                if len(self.prices) > self.WINDOW_SIZE: self.prices.pop(0)

                start_price, root_slope = self.regression_line(self.prices)
                fair_value = root_slope * (len(self.prices) - 1) + start_price

                # current_fair_price = self.START_PRICE + self.ROOT_SLOPE * state.timestamp (fixed true price)

                # Deviation from the trend line with linear scaling between order sizes -80 and 80

                raw = ((fair_value - mid_price) / self.MAX_VARIANCE) * self.LIMIT_QTY
                order_size = max(-self.LIMIT_QTY, min(self.LIMIT_QTY, raw))
                order_size = int(order_size)

                # Order size linearly dependant on the deviation from the trend line between 0 and 80.
                # order_size = (self.LIMIT_QTY / 2) * (1 - deviation / self.MAX_VARIANCE)
                # order_size = max(0, int(order_size))
              
                orders.append(Order(product, best_ask, order_size))

            elif product == "ASH_COATED_OSMIUM" and buy_orders and sell_orders:
                current_position = state.position.get(product, 0)

                best_bid = max(buy_orders)
                best_ask = min(sell_orders)
                
                current_market_spread = best_ask - best_bid

                if current_market_spread > 8:

                    #Penny the market to make orders which are first to get filled with max spread.
                    
                    buy_quote = best_bid + 1
                    sell_quote = best_ask - 1

                    if sell_quote <= buy_quote:
                        sell_quote = buy_quote + 1

                    # Limit size to whatever we can hold and using the volume analysis, use 13 order size to get max pnl
                
                    can_buy = self.LIMIT_QTY - current_position
                    can_sell = self.LIMIT_QTY + current_position
                    
                    orders.append(Order(product, buy_quote, min(self.ORDER_SIZE, can_buy)))
                    orders.append(Order(product, sell_quote, -min(self.ORDER_SIZE, can_sell)))

            result[product] = orders

        traderData = ""
        conversions = 0
        return result, conversions, traderData
    
    def regression_line(self, prices):
        n = len(prices)
        if n == 0:
            return self.START_PRICE, self.ROOT_SLOPE

        x = list(range(n))
        y = prices

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xx = sum(xi * xi for xi in x)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x) if (n * sum_xx - sum_x * sum_x) != 0 else 0
        intercept = (sum_y - slope * sum_x) / n if n != 0 else self.START_PRICE

        return intercept, slope