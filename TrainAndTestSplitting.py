import dataProcessing as dp
import random as rand
import pandas as pd
import csv

class TrainAndTestSplitting(object):
    def __init__(self,dataMatrix):
        self.numberOfInstances = len(dataMatrix)
        self.data              = dataMatrix
        self.dataTrain         = []
        self.dataTest          = []
        self.numberOfTrain     = None
        self.numberOfTest      = None
        self.trainSize         = None
        self.testSize          = None
        
    def DataProcess(self):
        # print(self.data)
        self.listUserId = list(set(self.data['userId'].values.tolist()))
        self.numberOfUser = len(self.listUserId)
        # self.dataValue = self.data['rating'].values.tolist()
        self.listIndex = self.data.index
        

    def RandomSplitting(self):
        self.DataProcess()
        shuffleList = [i for i in self.listIndex]
        rand.shuffle(shuffleList)
        for idxTrain in range(self.numberOfTrain):
            self.dataTrain.append([self.data['userId'][shuffleList[idxTrain]],self.data['name'][shuffleList[idxTrain]],self.data['rating'][shuffleList[idxTrain]]])
        # self.dataTrain = pd.DataFrame(data = self.dataTrain, columns = ["userId","name","rating"])    
        for idxTest in range(self.numberOfTest):
            self.dataTest.append([self.data['userId'][shuffleList[self.numberOfTrain + idxTest]],self.data['name'][shuffleList[self.numberOfTrain + idxTest]],self.data['rating'][shuffleList[self.numberOfTrain + idxTest]]])    
        # self.dataTest = pd.DataFrame(data = self.dataTest, columns = ["userId","name","rating"])    

    def trainAndTestSplitting(self, trainSize = 0.9, testSize = 0.1):
        if (trainSize + testSize > 1):
            return "ERROR: Train set and test size are too big!!!"
        self.trainSize = trainSize
        self.testSize = testSize
        self.numberOfTrain = int(self.trainSize * self.numberOfInstances)
        self.numberOfTest  = self.numberOfInstances - self.numberOfTrain
        self.RandomSplitting()
        self.writeCSV()

    def writeCSV(self):
        filenameTrain = "Train_steam_user.csv"
        with open(filenameTrain, 'w', encoding = 'utf-8', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(['userId','name','rating'])
            writer.writerows(self.dataTrain)

        filenameTest = "Test_steam_user.csv"
        with open(filenameTest, 'w', encoding = 'utf-8', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(['userId','name','rating'])
            writer.writerows(self.dataTest)   
       
    
t = TrainAndTestSplitting(dp.test.dataMatrix)
t.trainAndTestSplitting()
# print(t.dataTrain)