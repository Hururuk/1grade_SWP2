# import module
from datamanager import * # 파일관리를 위한 datamanager 모듈 사용
from datetime import datetime # 오늘 날짜를 가져오기 위해 datatime 모듈 사용
import pandas as pd # 주식의 종목코드를 가져오기 위해 pandas 모듈 사용
import FinanceDataReader as fdr # 주식의 가격을 불러오기 위해 FinanceDataReader 사용

# 전역변수
fileName = "database.dat" # 데이터를 저장할 파일명
stockCode = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0] # 주식 종목 코드를 저장하는 변수
# stockCode를 수정하여 주식 종목 코드를 불러올 수 있도록 사전 작업
stockCode = stockCode[['회사명', '종목코드']]
stockCode = stockCode.rename(columns={'회사명':'name', '종목코드':'code'})
stockCode.code = stockCode.code.map('{:06d}'.format)

# balance 클래스
class balance:
    def __init__(self, accountName, baseMoney): # 생성자
        self.accountName = accountName
        self.money = baseMoney
        self.stockList = {}
        self.saveAccount()

    def saveAccount(self): # saveAccount 함수
        dataFile = dataManager(fileName)
        dataList = dataFile.dataRead()
        for items in dataList:
            if items['AccountName'] == self.accountName:
                items['Money'] = self.money
                items['Stock'] = self.stockList
                dataFile.dataWrite(dataList)
                return
        dataList.append({'AccountName':self.accountName, 'Money':self.money, 'Stock':self.stockList})
        dataFile.dataWrite(dataList)

    def addMoney(self, n): # addMoney 함수
        self.money += n
        self.saveAccount()

    def delMoney(self, n): # delMoney 함수
        if (self.money >= n):
            self.money -= n
            self.saveAccount()
        else:
            return

    def showMoney(self): # showMoney 함수
        return self.money

    def showStockCode(self, name): # showStockCode 함수
        return stockCode[stockCode.name == name].code.values[0].strip()

    def showStockPrice(self, code): # showStockPrice 함수
        today = datetime.today().strftime('%Y-%m-%d') # 현재 날짜를 str 형태로 저장
        #시간에 따른 예외 처리 필요.
        # today = '2020-11-27'
        return fdr.DataReader(code, today)['Open'].values.tolist()[0]

    def addStock(self, name, amount): # addStock 함수
        price = int(self.showStockPrice(self.showStockCode(name))) * amount
        if self.money >= price :
            if name in self.stockList.keys():
                self.stockList[name] += amount
                self.money -= price
            else:
                self.stockList[name] = amount
                self.money -= price
            self.saveAccount()

    def delStock(self, name, amount): # delStock 함수
        price = int(self.showStockPrice(self.showStockCode(name))) * amount
        if name in self.stockList.keys() and self.stockList[name] >= amount:
            self.stockList[name] -= amount
            if self.stockList[name] == 0:
                del self.stockList[name]
            self.money += price
            self.saveAccount()

    def showStockList(self): # showStockList 함수
        return self.stockList

# Unit Test
if __name__ == '__main__':
    testaccount = balance("testAccount", 1000000)
    testaccount.addMoney(1000000)
    print(testaccount.showMoney())
    testaccount.delMoney(100000)
    print(testaccount.showMoney())
    testaccount.addStock("LG화학", 1)
    print(testaccount.showStockList())
    print(testaccount.showMoney())
    testaccount.delStock("LG화학", 1)
    print(testaccount.showStockList())
    print(testaccount.showMoney())