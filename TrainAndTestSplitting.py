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
        self.dataTrainPos       = []          
        self.dataTestingPos     = []          
        self.numberOfTrain     = None
        self.numberOfTest      = None
        self.trainSize         = None
        self.testSize          = None
        self.position           = {}
        self.listUserId        = None
        
    def DataProcess(self):
        self.listUserId = list(set(self.data['userId'].values.tolist()))
        self.userId = self.data['userId'].values.tolist()
        self.numberOfUser = len(self.listUserId)
        self.listIndex = self.data.index

    def StratifiedSplitting(self):
        for user in self.listUserId:
            self.position[user][1] /= self.numberOfInstances
            rand.shuffle(self.position[user][0])
            k = int(self.numberOfTrain * self.position[user][1])
            self.dataTrainPos.extend(self.position[user][0][: k])
            self.dataTestingPos.extend(self.position[user][0][k :])
        for idxTrain in self.dataTrainPos:
            self.dataTrain.append([self.data['userId'][idxTrain],self.data['name'][idxTrain],self.data['rating'][idxTrain]])
        for idxTest in self.dataTestingPos:
            self.dataTest.append([self.data['userId'][idxTest],self.data['name'][idxTest],self.data['rating'][idxTest]])  

    def countData(self):
        self.DataProcess()
        for user in self.listUserId:
            self.position[user] = [[], 0]
        for idx in range(self.numberOfInstances):
            user = self.userId[idx]
            self.position[user][0].append(idx)
            self.position[user][1] += 1     

    def RandomSplitting(self):
        self.DataProcess()
        shuffleList = [i for i in self.listIndex]
        rand.shuffle(shuffleList)
        for idxTrain in range(self.numberOfTrain):
            self.dataTrain.append([self.data['userId'][shuffleList[idxTrain]],self.data['name'][shuffleList[idxTrain]],self.data['rating'][shuffleList[idxTrain]]])
        for idxTest in range(self.numberOfTest):
            self.dataTest.append([self.data['userId'][shuffleList[self.numberOfTrain + idxTest]],self.data['name'][shuffleList[self.numberOfTrain + idxTest]],self.data['rating'][shuffleList[self.numberOfTrain + idxTest]]])    

    def trainAndTestSplitting(self, trainSize = 0.99, testSize = 0.01):
        if (trainSize + testSize > 1):
            return "ERROR: Train set and test size are too big!!!"
        self.trainSize = trainSize
        self.testSize = testSize
        self.numberOfTrain = int(self.trainSize * self.numberOfInstances)
        self.numberOfTest  = self.numberOfInstances - self.numberOfTrain
        # self.RandomSplitting()
        self.countData()
        self.StratifiedSplitting()
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
