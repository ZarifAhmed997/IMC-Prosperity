from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List

class Trader:
    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        
        LIMIT_QTY = 80
        START_TIMESTAMP = 0

        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []

            if product == "INTARIAN_PEPPER_ROOT":
                if state.timestamp == START_TIMESTAMP:
                    for ask_price, ask_qty in sorted(order_depth.sell_orders.items()):
                        current_position = state.position.get(product, 0)
                        room = LIMIT_QTY - current_position
                        if room <= 0: break
                        qty_to_buy = min(-ask_qty, room)  
                        orders.append(Order(product, ask_price, qty_to_buy))

            elif product == "ASH_COATED_OSMIUM":
                current_position = state.position.get(product, 0)
                if -LIMIT_QTY < current_position < LIMIT_QTY:
                    buy_prices = state.order_depths[product].buy_orders
                    sell_prices = state.order_depths[product].sell_orders
                    if buy_prices and sell_prices:
                        current_buy = min(buy_prices)
                        current_sell = max(sell_prices)
                        if current_buy - current_sell > 2:
                            orders.append(Order(product, current_buy + 1, 10))
                            orders.append(Order(product, current_sell - 1, -10))

            result[product] = orders

        traderData = ""
        conversions = 0
        return result, conversions, traderData