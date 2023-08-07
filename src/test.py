import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(parent_directory)

from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import *
import time
import threading
import position as Position
import strategy as Strategy
from collections import defaultdict
import csv

# input is dictionary of all positions
# output is dictionary of all positions bundled by ticker
# def bundlePositionsByTicker(all_positions:{}):
#     bundles = {}
#     for key, pos in all_positions.items():
#         ticker = pos.getContract().symbol
#         if ticker not in bundles:
#             bundles[ticker] = [pos]
#         else:
#             bundles[ticker].append(pos)
        
#     return bundles

def getStrategyMap(positionMap:{}):
    strategyMap = defaultdict()

    with open('positions.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader)
        for position in spamreader:

            conId = int(position[0])
            ticker = positionMap[conId].getContract().symbol 
            strategy = position[1]
            index = int(position[2])

            if (ticker, strategy) not in strategyMap:
                strategyMap[(ticker, strategy)] = [None] * 4

            strategyMap[(ticker, strategy)][index] = conId

    return strategyMap

def getStrategies(strategyMap:{}, positionMap:{}):
    strategies = defaultdict()

    for (ticker, strategy), positions in strategyMap.items():
        if ticker not in strategies:
            strategies[ticker] = []

        if strategy == "CoveredCall":
            stock = positionMap[ positions[0] ]
            call = positionMap[ positions[1] ]
            strategies[ticker].append(Strategy.CoveredCall(stock, call))

        elif strategy == "LongStock":
            stock = positionMap[ positions[0]]
            strategies[ticker].append(Strategy.LongStock(stock))

        elif strategy == "ShortPut":
            put = positionMap[ positions[0]]
            strategies[ticker].append(Strategy.ShortPut(put))

        elif strategy == "Future":
            future = positionMap[ positions[0]]
            strategies[ticker].append(Strategy.Future(future))

        elif strategy == "SyntheticLending":
            stock = positionMap[ positions[0] ]
            put = positionMap[ positions[1] ]
            call = positionMap[ positions[2] ]
            strategies[ticker].append(Strategy.SyntheticLending(stock, put, call))

        elif strategy == "BorrowBox":
            shortCall = positionMap[ positions[0] ]
            longPut = positionMap[ positions[1] ]
            longCall = positionMap[ positions[2] ]
            shortPut = positionMap[ positions[3] ]
            strategies[ticker].append(Strategy.BorrowBox(shortCall, longPut, longCall, shortPut))

    return strategies
            
# input is dictionary of all positions bundled by ticker
# output is dictionary of all strategies bundled by ticker
def mapPositionsToStrategies(positionMap:{}):
    strategyMap = getStrategyMap(positionMap)

    return getStrategies(strategyMap, positionMap)


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, wrapper=self)
        self.nextValidOrderId = None
        self.all_positions = {}
        self.posEnd = False

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("Error: {} {} {} {}".format(reqId, errorCode, errorString, advancedOrderRejectJson))

    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

    def position(self, account, contract, position, avgCost):
        self.all_positions[contract.conId] = Position.Position(account, contract, position, avgCost)

    def positionEnd(self):
        self.posEnd = True
        print("Successfully received all position data")

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7496, 0)

    t1 = threading.Thread(target=app.run)
    t1.start()

    # await TWS connection acknowledgement
    while (app.nextValidOrderId == None):
        time.sleep(1)
        print("Waiting for TWS connection acknowledgement ...")
    print("Connection Established")

    app.reqPositions() # associated callback: position
    print("Waiting for IB's API response for accounts positions requests...\n")

    # await get all positions (IBKR API only allows 50 items per call)
    while (app.posEnd == False):
        time.sleep(1)

    all_positions = app.all_positions

    # for key, position in all_positions.items():
        # position.print()

    strategyMap = mapPositionsToStrategies(all_positions)

    for ticker, strategies in strategyMap.items():
        for strategy in strategies:
            strategy.print()

    app.disconnect()

if __name__ == "__main__":
    main()