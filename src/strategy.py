from ibapi.wrapper import *
import position as Position
from abc import ABC, abstractmethod
 
class Strategy(ABC):
    @abstractmethod 
    def print(self): pass

    @abstractmethod 
    def getPosition(self): pass

class LongStock(Strategy):
    def __init__(self, stock:Position):
        self.stock = stock
    
    def print(self):
        print("\nLong Stock")
        print("Stock: {}".format(self.stock.print()))

    def getPosition(self):
        return [self.stock]
 
class CoveredCall(Strategy):
    def __init__(self, stock:Position, call:Position):
        self.stock = stock
        self.call = call
 
    def print(self):
        print("\nCovered Call")
        print("Stock: {}".format(self.stock.print()))
        print("Call: {}".format(self.call.print()))

    def getPosition(self):
        return [self.stock, self.call]
    
class ShortPut(Strategy):
    def __init__(self, put:Position):
        self.put = put
    
    def print(self):
        print("\nShort Put")
        print("Stock: {}".format(self.put.print()))

    def getPosition(self):
        return [self.put]
    
class Future(Strategy):
    def __init__(self, future:Position):
        self.future = future
    
    def print(self):
        print("\nFuture")
        print("Future: {}".format(self.future.print()))

    def getPosition(self):
        return [self.future]
    
class SyntheticLending(Strategy):
    def __init__(self, stock:Position, put:Position, call:Position):
        self.stock = stock
        self.call = call
        self.put = put
 
    def print(self):
        print("\nSynthetic Lending:")
        print("Stock: {}".format(self.stock.print()))
        print("Put: {}".format(self.put.print()))
        print("Call: {}".format(self.call.print()))

    def getPosition(self):
        return [self.stock, self.put, self.call]
    
class BorrowBox(Strategy):
    def __init__(self, shortCall:Position, longPut:Position, longCall:Position, shortPut:Position):
        self.shortCall = shortCall
        self.longPut = longPut
        self.longCall = longCall
        self.shortPut = shortPut
 
    def print(self):
        print("\nBorrow Box:")
        print("Short Call: {}".format(self.shortCall.print()))
        print("Long Put: {}".format(self.longPut.print()))
        print("Long Call: {}".format(self.longCall.print()))
        print("Short Put: {}".format(self.shortPut.print()))

    def getPosition(self):
        return [self.shortCall, self.longPut, self.longCall, self.shortPut]

 
