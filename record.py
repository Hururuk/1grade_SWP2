# import module
from datamanager import *
from datetime import datetime
from balance import *

# 전역변수
fileName = "ratioData.dat" # 데이터를 저장할 파일

# record 클래스
class record:
    def __init__(self, accountName): # 생성자
        self.accountName = accountName

    def saveAccount(self, mode): # saveAccount 함수
        # mode = 0 - money / mode = 1 - stock
        time = datetime.today().strftime("%Y-%m-%d %H:%M:%S") # 현재 날짜를 str 형태로 저장
        dataFile = dataManager(fileName)
        dataList = dataFile.dataRead()
        for items in dataList:
            if items['AccountName'] == self.accountName:
                if(mode == 0):
                    items['Money'].append([self.money, time, self.balance])
                if(mode == 1):
                    items['Stock'].append([self.stock, time, self.balance])
                dataFile.dataWrite(dataList)
                return
        dataList.append({'AccountName':self.accountName, 'Money':[[self.money, time, self.balance]], 'Stock':[]})
        dataFile.dataWrite(dataList)

    def recordBalanceChange(self, n, balance): # recordBalanceChange 함수
        self.money = n
        self.balance = balance
        self.saveAccount(0)

    def recordStockChange(self, n, balance): # recordStockChange 함수
        self.stock = n
        self.balance = balance
        self.saveAccount(1)

    def readBalanceChange(self): # readBalanceChange 함수
        dataFile = dataManager(fileName)
        dataList = dataFile.dataRead()
        for items in dataList:
            if items['AccountName'] == self.accountName:
                return items['Money']

    def readStockChange(self): # readStockChange 함수
        dataFile = dataManager(fileName)
        dataList = dataFile.dataRead()
        for items in dataList:
            if items['AccountName'] == self.accountName:
                return items['Stock']
            
# Unit Test
if __name__ == '__main__':
    testAccount2 = record("tester2")
    testAccount2.recordBalanceChange(100000, 100000)
    testAccount2.recordStockChange(10000, 10000)
    print(testAccount2.readBalanceChange())
    print(testAccount2.readStockChange())