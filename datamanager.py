# import module
import pickle # 파일의 입출력을 위한 pickle 모듈 사용

# dataManager 클래스
class dataManager:
    def __init__(self, fn): # 생성자
        self.dataFileName = fn

    def dataRead(self): # dataRead 함수
        try:
            with open(self.dataFileName, 'rb') as fr:
                data = pickle.load(fr)
            return data
        except FileNotFoundError :
            return []

    def dataWrite(self, content): # dataWrite 함수
        with open(self.dataFileName, 'wb') as fw:
            pickle.dump(content, fw)

    def dataName(self): # dataName 함수
        return self.dataFileName

    def dataNameChange(self, fn): # dataNameChange 함수
        self.dataFileName = fn

# Unit Test
if __name__ == '__main__':
    dataManagertest = dataManager('testFile.dat')
    testData = [{'Name':'홍길동','Age':17}, {'Name':'김나영','Age':26}]
    dataManagertest.dataWrite(testData)
    print(dataManagertest.dataRead()[0]['Name'])
    print(dataManagertest.dataRead())