from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from balance import balance
from datamanager import dataManager
from record import record
from graphrecord import graphrecord
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setupUI()

        self.accounts = {}
        self.records = {}
        self.dm = dataManager('database.dat')
        self.initAccounts()

    # 레이아웃 설정 #
    def setupUI(self):
        self.layoutDialog = QVBoxLayout()

        self.setRow1UI()
        self.setRow2UI()
        self.setRow3UI()
        self.setSystemAlertUI()

        self.setLayout(self.layoutDialog)
        self.setWindowTitle("나만의 자산관리 프로그램")

    # 첫 번째 줄 레이아웃 #
    def setRow1UI(self):
        # 계좌 목록
        self.twAccountInfo = QTableWidget()
        self.twAccountInfo.setColumnCount(2)
        self.twAccountInfo.setHorizontalHeaderLabels(['계좌 번호', '총 자산'])
        self.twAccountInfo.resizeColumnsToContents()

        # 입출금
        self.cbDnW = QComboBox()
        self.cbDnW.addItems(['입금', '출금'])
        self.cbDnW.setCurrentIndex(0)
        self.leAmount = QLineEdit()
        pbSaveCash = QPushButton('현금 저장')
        pbSaveCash.clicked.connect(self.submitDnW)

        layoutInputAmount = QHBoxLayout()
        layoutInputAmount.addWidget(QLabel('액수:'))
        layoutInputAmount.addWidget(self.leAmount)
        
        # 주식
        self.leAmountStock = QLineEdit()
        self.leStockName = QLineEdit()
        pbSaveStock = QPushButton('주식 저장')
        pbSaveStock.clicked.connect(self.submitSaveStock)

        layoutInputAmountStock = QHBoxLayout()
        layoutInputAmountStock.addWidget(QLabel('변동주:'))
        layoutInputAmountStock.addWidget(self.leAmountStock)
        
        layoutInputStockName = QHBoxLayout()
        layoutInputStockName.addWidget(QLabel('주식명:'))
        layoutInputStockName.addWidget(self.leStockName)
        
        # 계좌 추가
        self.leNewAccountName = QLineEdit()
        self.leNewAccountBaseMoney = QLineEdit()
        pbSubmitNewAccount = QPushButton('계좌 등록')
        pbSubmitNewAccount.clicked.connect(self.submitNewAccount)

        layoutInputNewAccountName = QHBoxLayout()
        layoutInputNewAccountName.addWidget(QLabel('계좌 번호:'))
        layoutInputNewAccountName.addWidget(self.leNewAccountName)

        layoutInputNewAccountBaseMoney = QHBoxLayout()
        layoutInputNewAccountBaseMoney.addWidget(QLabel('예수금:'))
        layoutInputNewAccountBaseMoney.addWidget(self.leNewAccountBaseMoney)

        # 계좌 선택
        self.cbAccounts = QComboBox()
        self.cbAccounts.setFixedWidth(150)
        self.cbAccounts.addItem('---------------')
        self.cbAccounts.currentIndexChanged.connect(self.displayBreakdownList)

        layoutChoiceAccount = QHBoxLayout()
        layoutChoiceAccount.addStretch()
        layoutChoiceAccount.addWidget(QLabel('선택 계좌:'))
        layoutChoiceAccount.addWidget(self.cbAccounts)

        # 배치
        layoutRow = QGridLayout()
        layoutRow.addWidget(QLabel('계좌 목록'), 0, 0, alignment=Qt.AlignCenter)
        layoutRow.addWidget(self.twAccountInfo, 1, 0, -1, 1)
        layoutRow.addWidget(QLabel('현금'), 0, 1, alignment=Qt.AlignCenter)
        layoutRow.addWidget(self.cbDnW, 1, 1)
        layoutRow.addLayout(layoutInputAmount, 2, 1)
        layoutRow.addWidget(pbSaveCash, 3, 1)
        layoutRow.addWidget(QLabel('주식'), 0, 2, alignment=Qt.AlignCenter)
        layoutRow.addLayout(layoutInputAmountStock, 1, 2)
        layoutRow.addLayout(layoutInputStockName, 2, 2)
        layoutRow.addWidget(pbSaveStock, 3, 2)
        layoutRow.addWidget(QLabel('새 계좌 등록'), 0, 3, alignment=Qt.AlignCenter)
        layoutRow.addLayout(layoutInputNewAccountName, 1, 3)
        layoutRow.addLayout(layoutInputNewAccountBaseMoney, 2, 3)
        layoutRow.addWidget(pbSubmitNewAccount, 3, 3)
        layoutRow.addLayout(layoutChoiceAccount, 4, 1, 1, -1, alignment=Qt.AlignRight)

        self.layoutDialog.addLayout(layoutRow)

    # 두 번째 줄 레이아웃 #
    def setRow2UI(self):
        # 거래 내역 목록
        self.twBreakdown = QTableWidget()
        self.twBreakdown.setColumnCount(4)
        self.twBreakdown.setHorizontalHeaderLabels(['유형', '변동 내용', '잔고', '날짜'])
        self.twBreakdown.setColumnWidth(0, 110)
        self.twBreakdown.setColumnWidth(1, 200)
        self.twBreakdown.setColumnWidth(2, 300)
        self.twBreakdown.setColumnWidth(3, 230)
        self.layoutDialog.addWidget(self.twBreakdown)

    # 세 번째 줄 레이아웃 #
    def setRow3UI(self):
        # 그래프
        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        # 날짜 선택
        self.cbStartDate = QComboBox()
        self.cbStartDate.setFixedWidth(120)
        self.cbStartDate.addItem('---------------')
        self.cbEndDate = QComboBox()
        self.cbEndDate.setFixedWidth(120)
        self.cbEndDate.addItem('---------------')
        pbCalc = QPushButton('계산')
        pbCalc.clicked.connect(self.displayGraph)
        # 배치
        layoutSelectDate = QVBoxLayout()
        layoutSelectDate.addStretch()
        layoutSelectDate.addWidget(self.cbStartDate)
        layoutSelectDate.addWidget(self.cbEndDate)
        layoutSelectDate.addWidget(pbCalc)
        layoutSelectDate.addStretch()

        layoutRow = QHBoxLayout()
        layoutRow.addWidget(self.canvas, stretch=1)
        layoutRow.addLayout(layoutSelectDate)

        self.layoutDialog.addLayout(layoutRow)

    # 시스템 알림 레이아웃 #
    def setSystemAlertUI(self):
        self.lbSystemAlert = QLabel('시스템 알림')
        self.lbSystemAlert.setAlignment(Qt.AlignCenter)

        self.layoutDialog.addWidget(self.lbSystemAlert)

    # 현금 입출금 #
    def submitDnW(self):
        cmd = self.cbDnW.currentText()
        amount = self.leAmount.text()
        account = self.cbAccounts.currentText()
        if not amount:
            self.showWarningMsgBox(f'{cmd}할 액수를 작성해 주세요.')
        elif not amount.isdecimal():
            self.showWarningMsgBox('액수에는 숫자만 입력해 주세요.')
        elif not self.cbAccounts.currentIndex():
            self.showWarningMsgBox(f'{cmd}할 계좌를 선택해 주세요.')
        else:
            curAccount = self.accounts[account]
            curRecord = self.records[account]
            if cmd == '입금':
                curAccount.addMoney(int(amount))
                curRecord.recordBalanceChange(int(amount), curAccount.money)
            else:
                if curAccount.money >= int(amount):
                    curAccount.delMoney(int(amount))
                    curRecord.recordBalanceChange(-int(amount), curAccount.money)
                else:
                    self.showWarningMsgBox('계좌 잔고가 부족합니다.')
                    return
            self.refreshAccountsList('MODIFY')
            self.leAmount.clear()
            self.showInfoMsgBox(f'{cmd}이 완료되었습니다.')

    # 주식 저장 #
    def submitSaveStock(self):
        amount = self.leAmountStock.text()
        stockName = self.leStockName.text()
        account = self.cbAccounts.currentText()
        if not amount or not stockName:
            self.showWarningMsgBox('변동주와 주식명 모두 입력해 주세요.')
        elif not (('-' in amount and amount[1:].isdecimal()) or amount.isdecimal()):
            self.showWarningMsgBox('변동주에는 양이나 음의 정수만 입력해 주세요.')
        elif not self.cbAccounts.currentIndex():
            self.showWarningMsgBox('주식을 저장할 계좌를 선택해 주세요.')
        else:
            amount = int(amount)
            curAccount = self.accounts[account]
            curRecord = self.records[account]
            price = int(curAccount.showStockPrice(curAccount.showStockCode(stockName)))*amount
            if amount >= 0:
                if curAccount.money >= price:
                    curAccount.addStock(stockName, amount)
                    curRecord.recordStockChange(amount, curAccount.money)
                else:
                    self.showWarningMsgBox('계좌 잔액이 부족합니다.')
                    return
            else:
                amount = abs(amount)
                if stockName not in curAccount.stockList.keys():
                    self.showWarningMsgBox('해당 계좌는 해당 주식을 보유하고 있지 않습니다.')
                    return
                elif amount > curAccount.stockList[stockName]:
                    self.showWarningMsgBox('입력값이 해당 계좌의 해당 주식 보유량을 초과하였습니다.')
                    return
                else:
                    curAccount.delStock(stockName, amount)
                    curRecord.recordStockChange(-amount, curAccount.money)
            self.refreshAccountsList('MODIFY')
            self.leAmountStock.clear()
            self.leStockName.clear()
            self.showInfoMsgBox('주식 저장이 완료되었습니다.')

    # 계좌 생성 #
    def submitNewAccount(self):
        account = self.leNewAccountName.text()
        baseMoney = self.leNewAccountBaseMoney.text()
        if not account or not baseMoney:
            self.showWarningMsgBox('계좌 번호와 기초 자금 모두 입력해 주세요.')
        elif account in self.accounts.keys():
            self.showWarningMsgBox('이미 존재하는 계좌입니다.')
        elif not baseMoney.isdecimal():
            self.showWarningMsgBox('기초 자금에는 숫자만 입력해 주세요.')
        else:
            self.accounts[account] = balance(account, int(baseMoney))
            self.records[account] = record(account)
            self.records[account].recordBalanceChange(int(baseMoney), self.accounts[account].money)
            self.refreshAccountsList('ADD')
            self.leNewAccountName.clear()
            self.leNewAccountBaseMoney.clear()
            self.showInfoMsgBox('새 계좌가 추가되었습니다.')

    # 거래 내역 출력 #
    def displayBreakdownList(self):
        if self.cbAccounts.currentIndex():
            self.twBreakdown.clearContents()
            self.twBreakdown.setRowCount(0)
            self.twBreakdown.setColumnWidth(0, 110)
            self.twBreakdown.setColumnWidth(1, 200)
            self.twBreakdown.setColumnWidth(2, 300)
            self.twBreakdown.setColumnWidth(3, 230)
            
            curRecord = self.records[self.cbAccounts.currentText()]
            datas = [{'type': '입출금', 'changed': data[0], 'balance': data[2], 'time': data[1]} for data in curRecord.readBalanceChange()] + [{'type': '주식', 'changed': data[0], 'balance': data[2], 'time': data[1]} for data in curRecord.readStockChange()]
            datas = sorted(datas, key=lambda x: x['time'], reverse=True)

            for data in datas:
                row = self.twBreakdown.rowCount()
                self.twBreakdown.setRowCount(row+1)
                item = QTableWidgetItem(data['type'])
                item.setTextAlignment(Qt.AlignCenter)
                self.twBreakdown.setItem(row, 0, QTableWidgetItem(data['type']))
                item = QTableWidgetItem(f"{int(data['changed']):,}")
                item.setTextAlignment(Qt.AlignCenter)
                self.twBreakdown.setItem(row, 1, item)
                item = QTableWidgetItem(f"{int(data['balance']):,}")
                item.setTextAlignment(Qt.AlignCenter)
                self.twBreakdown.setItem(row, 2, item)
                item = QTableWidgetItem(data['time'])
                item.setTextAlignment(Qt.AlignCenter)
                self.twBreakdown.setItem(row, 3, item)
            #self.setBreakdownHeaderWidth()

            dates = [data['time'].split()[0] for data in datas]
            dates = sorted(list(set(dates)))
            self.cbStartDate.clear()
            self.cbStartDate.addItem('---------------')
            self.cbStartDate.addItems(dates)
            dates.reverse()
            self.cbEndDate.clear()
            self.cbEndDate.addItem('---------------')
            self.cbEndDate.addItems(dates)
        else:
            self.twBreakdown.clearContents()
            self.twBreakdown.setRowCount(0)

    # 그래프 출력 #
    def displayGraph(self):
        if self.cbStartDate.currentIndex() and self.cbEndDate.currentIndex():
            gr = graphrecord('', self.cbAccounts.currentText())
            self.fig.clear()
            gr.showMoneyStockGraph(self.fig, self.cbStartDate.currentText(), self.cbEndDate.currentText())
            self.canvas.draw()
        else:
            self.showWarningMsgBox('날짜를 모두 선택해 주세요.')

    # 경고 메시지 박스 #
    def showWarningMsgBox(self, msg):
        QMessageBox.warning(self, '알림', msg)

    # 완료 메시지 박스 #
    def showInfoMsgBox(self, msg):
        QMessageBox.information(self, '알림', msg)

    # 계좌 목록 초기화 #
    def initAccounts(self):
        accountDatas = self.dm.dataRead()
        if len(accountDatas):
            self.refreshAccountsList('INIT', accountDatas=accountDatas)
            for data in accountDatas:
                account = data['AccountName']
                money = data['Money']
                stock = data['Stock']

                self.accounts[account] = balance(account, money)
                self.accounts[account].stockList = stock
                self.accounts[account].saveAccount()
                self.records[account] = record(account)

    # 계좌 목록 갱신 #
    def refreshAccountsList(self, cmd, accountDatas=None):
        if accountDatas is None:
            accountDatas = self.dm.dataRead()
        if not len(accountDatas):
            return
        if cmd == 'INIT':
            for data in accountDatas:
                self.cbAccounts.addItem(data['AccountName'])
                row = self.twAccountInfo.rowCount()
                self.twAccountInfo.setRowCount(row+1)
                self.twAccountInfo.setItem(row, 0, QTableWidgetItem(data['AccountName']))
                self.twAccountInfo.setItem(row, 1, QTableWidgetItem(f"{data['Money']:,}"))
        elif cmd == 'ADD':
            self.cbAccounts.addItem(self.leNewAccountName.text())
            row = self.twAccountInfo.rowCount()
            self.twAccountInfo.setRowCount(row+1)
            self.twAccountInfo.setItem(row, 0, QTableWidgetItem(self.leNewAccountName.text()))
            self.twAccountInfo.setItem(row, 1, QTableWidgetItem(f"{int(self.leNewAccountBaseMoney.text()):,}"))
        elif cmd == 'MODIFY':
            row = self.twAccountInfo.findItems(self.cbAccounts.currentText(), Qt.MatchExactly)[0].row()
            self.twAccountInfo.setItem(row, 1, QTableWidgetItem(f"{self.accounts[self.cbAccounts.currentText()].money:,}"))
        self.setAccountInfoHeaderWidth()

    # 계좌 목록 컬럼 너비 설정 #
    def setAccountInfoHeaderWidth(self):
        header = self.twAccountInfo.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

    # 거래 내역 컬럼 너비 설정 #
    def setBreakdownHeaderWidth(self):
        header = self.twBreakdown.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()