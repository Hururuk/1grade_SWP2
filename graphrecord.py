# import module
import matplotlib.pyplot as plt
import numpy as np
from record import *
from datamanager import *

# 전역변수
fileName = "ratioData.dat" # 데이터를 읽어오는 파일

# graphrecord 클래스
class graphrecord:
    def __init__(self, graphname, accountName):
        # type = 'Money' or 'Stock'
        self.name = graphname
        self.accountName = accountName
        self.recordDB = []
        self.recordDB = self.readRecordDB()

    def readRecordDB(self):
        dataFile = dataManager(fileName)
        dataList = dataFile.dataRead()
        return dataList

    def showMoneyStockGraph(self, fig, start, end):
        start = start + ' 00:00:00'
        end = end + ' 23:59:59'
        moneyList = []
        stockList = []
        for items in self.recordDB:
            if items['AccountName'] == self.accountName:
                moneyList = items['Money']
                stockList = items['Stock']
                break
        x_values = []
        #날짜 불러오기
        for value in moneyList:
            if start <= value[1] <= end:
                x_values.append(value[1])
        y_values = []
        #금액 불러오기
        for value in moneyList:
            if start <= value[1] <= end:
                y_values.append(value[0])
        m_values = []
        #날짜 불러오기
        for value in stockList:
            if start <= value[1] <= end:
                m_values.append(value[1])
        n_values = []
        #금액 불러오기
        for value in stockList:
            if start <= value[1] <= end:
                n_values.append(value[0])

        # fig = plt.Figure()
        money_plot = fig.add_subplot(211)
        money_plot.plot(x_values, y_values, color='green', marker='o') #money 그래프
        stock_plot = fig.add_subplot(212)
        stock_plot.plot(m_values, n_values, color='gray', marker='o') #stock 그래프

        # plt.show() #디버깅용(그래프 바로 보여주기)
        # return fig
        # 그래프를 png파일로 저장
        # plt.draw()
        # fig = plt.gcf()
        # fig.savefig(self.name, dpi=fig.dpi)

# Unit Test
if __name__ == '__main__':
    tester = graphrecord('TestGraph', 'tester2')
    tester.showMoneyStockGraph()