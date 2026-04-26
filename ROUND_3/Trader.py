from datamodel import OrderDepth, TradingState, Order
from typing import List, Dict
import math as m


class Trader:

    def __init__(self):

        # ------------------------
        # RISK
        # ------------------------
        self.LIMIT = 80
        self.order_size = 12

        # ------------------------
        # WINDOWS
        # ------------------------
        self.fast_window = 10
        self.slow_window = 50

        self.prices: Dict[str, List[float]] = {}

    # ------------------------
    # MID PRICE
    # ------------------------
    def mid(self, od: OrderDepth):
        if not od.buy_orders or not od.sell_orders:
            return None
        return (max(od.buy_orders) + min(od.sell_orders)) / 2

    # ------------------------
    # UPDATE SERIES
    # ------------------------
    def update(self, product, price):
        if product not in self.prices:
            self.prices[product] = []

        self.prices[product].append(price)

        max_len = self.slow_window + 5
        if len(self.prices[product]) > max_len:
            self.prices[product].pop(0)

    # ------------------------
    # MEAN CALC
    # ------------------------
    def mean(self, arr):
        return sum(arr) / len(arr) if arr else 0

    # ------------------------
    # SLOPE (simple regression)
    # ------------------------
    def slope(self, arr):
        n = len(arr)
        if n < 2:
            return 0

        x = list(range(n))
        y = arr

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xx = sum(i * i for i in x)
        sum_xy = sum(i * j for i, j in zip(x, y))

        denom = n * sum_xx - sum_x * sum_x
        if denom == 0:
            return 0

        return (n * sum_xy - sum_x * sum_y) / denom

    # ------------------------
    # REGIME CLASSIFIER
    # ------------------------
    def regime(self, arr):

        if len(arr) < self.slow_window:
            return "neutral"

        fast = self.mean(arr[-self.fast_window:])
        slow = self.mean(arr[-self.slow_window:])

        trend = self.slope(arr[-self.slow_window:])

        divergence = fast - slow

        # thresholds (tunable)
        if abs(trend) > 0.3:
            return "trend"
        elif abs(divergence) > 3:
            return "mean_revert"
        else:
            return "neutral"

    # ------------------------
    # MAIN LOOP
    # ------------------------
    def run(self, state: TradingState):

        result: Dict[str, List[Order]] = {}

        for product in ["VELVETFRUIT_EXTRACT", "HYDROGEL_PACK"]:

            if product not in state.order_depths:
                continue

            od = state.order_depths[product]
            mid = self.mid(od)
            if mid is None:
                continue

            self.update(product, mid)

            arr = self.prices[product]
            regime = self.regime(arr)

            position = state.position.get(product, 0)

            best_bid = max(od.buy_orders)
            best_ask = min(od.sell_orders)

            orders: List[Order] = []

            # =====================================================
            # 1. MEAN REVERSION REGIME
            # =====================================================
            if regime == "mean_revert":

                fast = self.mean(arr[-self.fast_window:])
                slow = self.mean(arr[-self.slow_window:])

                z = (mid - slow)

                if z > 2:
                    qty = min(self.order_size, self.LIMIT + position)
                    orders.append(Order(product, best_bid, -qty))

                elif z < -2:
                    qty = min(self.order_size, self.LIMIT - position)
                    orders.append(Order(product, best_ask, qty))

            # =====================================================
            # 2. MOMENTUM REGIME
            # =====================================================
            elif regime == "trend":

                trend = self.slope(arr[-self.slow_window:])

                if trend > 0:
                    qty = min(self.order_size, self.LIMIT - position)
                    orders.append(Order(product, best_ask, qty))

                elif trend < 0:
                    qty = min(self.order_size, self.LIMIT + position)
                    orders.append(Order(product, best_bid, -qty))

            # =====================================================
            # 3. NEUTRAL (do nothing)
            # =====================================================
            else:
                pass

            result[product] = orders

        return result, 0, ""