from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import numpy
import math as Math

class Trader:
    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        
        LIMIT_QTY = 80

        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            current_position = state.position.get(product, 0)
            buy_orders = order_depth.buy_orders
            sell_orders = order_depth.sell_orders

            if product == "INTARIAN_PEPPER_ROOT" and buy_orders and sell_orders:
                current_position = state.position.get(product, 0)
                remaining_capacity = LIMIT_QTY - current_position

                for ask_price, ask_qty in sorted(order_depth.sell_orders.items()):
                    if remaining_capacity <= 0: break

                    available_qty = -ask_qty
                    trade_qty = min(available_qty, remaining_capacity)

                    if trade_qty > 0:
                        orders.append(Order(product, ask_price, trade_qty))
                        remaining_capacity -= trade_qty


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
                
                    can_buy = LIMIT_QTY - current_position
                    can_sell = LIMIT_QTY + current_position

                    order_size = 13
                    
                    orders.append(Order(product, buy_quote, min(order_size, can_buy)))
                    orders.append(Order(product, sell_quote, -min(order_size, can_sell)))

            result[product] = orders

        traderData = ""
        conversions = 0
        return result, conversions, traderData