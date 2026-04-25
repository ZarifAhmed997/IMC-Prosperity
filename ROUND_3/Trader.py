from datamodel import OrderDepth, TradingState, Order
import numpy as np

class Trader:

    def __init__(self):
        self.history = {}  # store mispricing history per product
        self.LIMIT_QTY = 80
        self.ORDER_SIZE = 13
        self.WINDOW_SIZE = 50
        self.prices = []

    def run(self, state: TradingState):
        result = {}

        underlying_price = None

# Get underlying price first
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders = []
            current_position = state.position.get(product, 0)
            buy_orders = order_depth.buy_orders
            sell_orders = order_depth.sell_orders
            from itertools import product

from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import math as Math

class Trader:

    def __init__(self):
        self.LIMIT_QTY = 80
        self.START_PRICE = None
        self.ORDER_SIZE = 13
        self.ROOT_SLOPE = 0.00145
        self.MAX_VARIANCE = 28
        self.WINDOW_SIZE = 50
        self.prices = []

        self.total_orders = 0
        self.total_buy_orders = 0
        self.total_sell_orders = 0

    def bid(self):
        return 10000

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

                    if trade_qty > 0 and ask_price % 1000 >  990 or ask_price % 1000 < 10:
                        orders.append(Order(product, ask_price, trade_qty))
                        remaining_capacity -= trade_qty
            '''
                
            if product == "VELVETFRUIT_EXTRACT" or product == 'HYDROGEN_PACK' and buy_orders and sell_orders:
                current_position = state.position.get(product, 0)

                if self.START_PRICE is None:
                    self.START_PRICE = (max(buy_orders) + min(sell_orders)) / 2
                
                best_bid = max(buy_orders)
                best_ask = min(sell_orders)
                mid_price = (best_bid + best_ask) / 2

                self.prices.append(mid_price)
                if len(self.prices) > self.WINDOW_SIZE: self.prices.pop(0)

                # start_price, root_slope = self.regression_line(self.prices)
                # fair_value = root_slope * (len(self.prices) - 1) + start_price

                intercept, slope = self.regression_line(self.prices)
                fair_value = intercept + slope * state.timestamp

                # Deviation from the trend line with linear scaling between order sizes -80 and 80

                raw = ((fair_value - mid_price) / self.MAX_VARIANCE) * self.LIMIT_QTY
                order_size = max(-self.LIMIT_QTY, min(self.LIMIT_QTY, raw))
                order_size = int(order_size)

                # Order size linearly dependant on the deviation from the trend line between 0 and 80.
                # order_size = (self.LIMIT_QTY / 2) * (1 - deviation / self.MAX_VARIANCE)
                # order_size = max(0, int(order_size))
            
                orders.append(Order(product, best_ask, order_size))

                print(f"Timestamp: {state.timestamp} | Total Orders: {self.total_orders} | Buys: {self.total_buy_orders} | Sells: {self.total_sell_orders} | Position: {current_position} | Mid: {mid_price:.2f} | Fair: {fair_value:.2f} | Deviation: {mid_price - fair_value:.2f}")

            if "VELVETFRUIT_EXTRACT" in state.order_depths:
                depth = state.order_depths["VELVETFRUIT_EXTRACT"]
                if depth.buy_orders and depth.sell_orders:
                    best_bid = max(depth.buy_orders)
                    best_ask = min(depth.sell_orders)
                    underlying_price = (best_bid + best_ask) / 2

            if product.startswith("VEV_") and buy_orders and sell_orders and underlying_price is not None:

                strike = int(product.split("_")[1])

                best_bid = max(buy_orders)
                best_ask = min(sell_orders)
                mid_price = (best_bid + best_ask) / 2

                # --- intrinsic value ---
                intrinsic = max(0, underlying_price - strike)

                mispricing = mid_price - intrinsic

                # --- store history per product ---
                if product not in self.prices:
                    self.prices.append({})

                if product not in self.prices[-1]:
                    self.prices[-1][product] = []

                history = self.prices[-1][product]
                history.append(mispricing)

                if len(history) > self.WINDOW_SIZE:
                    history.pop(0)

                if len(history) < 10:
                    continue

                mean = sum(history) / len(history)
                variance = sum((x - mean) ** 2 for x in history) / len(history)
                std = Math.sqrt(variance)

                if std == 0:
                    continue

                z = (mispricing - mean) / std

                # --- time decay adjustment ---
                TTE = max(1, 7 - state.timestamp // 1000000)
                decay_factor = TTE / 7

                fair_mispricing = mean * decay_factor

                deviation = mispricing - fair_mispricing

                raw = (-deviation / (std + 1e-6)) * self.LIMIT_QTY
                order_size = int(max(-self.LIMIT_QTY, min(self.LIMIT_QTY, raw)))

                # --- position control ---
                can_buy = self.LIMIT_QTY - current_position
                can_sell = self.LIMIT_QTY + current_position

                if order_size > 0:
                    qty = min(order_size, can_buy, self.ORDER_SIZE)
                    if qty > 0:
                        orders.append(Order(product, best_ask, qty))

                elif order_size < 0:
                    qty = min(-order_size, can_sell, self.ORDER_SIZE)
                    if qty > 0:
                        orders.append(Order(product, best_bid, -qty))

        return result, 0, ""
    
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