from ibapi.wrapper import *

class Position:
    def __init__(self, account:str, contract:Contract, position:Decimal, avgCost:float):
        self.account = account
        self.contract = contract 
        self.position = position
        self.avgCost = avgCost

    def print(self): print(self.account, self.contract, self.position, self.avgCost)

    def getAccount(self): return self.account
    def getContract(self): return self.contract
    def getPosition(self): return self.position
    def getAvgCost(self): return self.avgCost