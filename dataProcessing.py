import pandas as pd
import numpy as np


class dataProcessing(object):
    def __init__ (self, listUserFile, notTrain = True):
        self.listUserFile      = listUserFile
        self.dataGame          = None
        self.dataUserId        = None
        self.listNameGame      = None
        self.listGame          = None
        self.dataUser          = None
        self.listUser          = None
        self.listUserId        = None
        self.listBehavior      = None
        self.listHourPlayed    = None
        self.averagePlayedTime = None
        self.numberOfUser      = None
        self.numberOfGame      = None      
        self.dataMatrix        = None
        self.dataTable         = None
        self.notTrain          = notTrain
        self.dataMatrixTest    = None

    def PreProcessingCSV(self):
        if self.notTrain:
            self.dataUser = pd.read_csv(self.listUserFile)
            self.listUser = self.dataUser.drop(columns = ["0"])
            self.listUser = self.listUser[(self.listUser['behavior'] == 'play')]
            self.listUser = self.listUser[self.listUser.groupby('name').userId.transform(len) >= 20]
            self.listUser = self.listUser[self.listUser.groupby('userId').name.transform(len) >= 10]
            self.listGame = list(set(self.listUser['name'].values.tolist()))
            self.listGame = pd.DataFrame(data = self.listGame, columns = ['name'])
            self.dataGame = self.listGame
            self.numberOfGame = len(self.listGame)
            self.listUserId = self.listUser.drop(columns = ["name", "behavior", "hours"])
            self.listUserId = list(set(self.listUserId['userId'].values.tolist()))
            self.listUserId = pd.DataFrame(data = self.listUserId, columns = ['userId'])
            self.numberOfUser = len(self.listUserId)
            self.listBehavior = self.listUser.drop(columns = ["userId", "name", "hours"])
        else:
            self.dataMatrix = pd.read_csv("Train_" + self.listUserFile)
            self.dataMatrixTest = pd.read_csv("Test_" + self.listUserFile)
            self.listUserId = list(set(self.dataMatrixTest['userId'].values.tolist()))
            self.dataUserId = pd.DataFrame(data = self.listUserId, columns = ['userId'])
            self.listGame = list(set(self.dataMatrix['name'].values.tolist()))
            self.dataGame = pd.DataFrame(data = self.listGame, columns = ['name'])

    def CreateDataMatrix(self):
        if self.notTrain:
            self.dataTable = self.listGame.merge(self.listUser, how = 'left', on = 'name')
            self.dataMatrix = self.dataTable.drop(columns = ["behavior","hours","avg_hourplayed"])
            self.dataMatrix = self.dataMatrix[(self.dataMatrix["userId"].notnull())]
            self.listUser = self.listUser.drop(columns = ["behavior"])

    def CalAveragePlayedTime(self):
        if self.notTrain:
            self.listUser['name'].nunique()
            self.listUser['name'] = self.listUser['name'].astype(str)
            self.averagePlayedTime = self.listUser.groupby(['name'], as_index = False).hours.mean()
            self.averagePlayedTime['avg_hourplayed'] = self.averagePlayedTime['hours']
            self.averagePlayedTime.drop(columns = 'hours', inplace = True)
            self.listUser = self.listUser.merge(self.averagePlayedTime, how = 'left', on = 'name')

    def CalRatingGame(self):
        if self.notTrain:
            condition = [
                    self.listUser['hours'] >= (1.5 * self.listUser['avg_hourplayed']),
                    (self.listUser['hours'] >= 1 * self.listUser['avg_hourplayed']) & (self.listUser['hours'] < 1.5 * self.listUser['avg_hourplayed']),
                    (self.listUser['hours'] >= 0.6 * self.listUser['avg_hourplayed']) & (self.listUser['hours'] < 1 * self.listUser['avg_hourplayed']),
                    (self.listUser['hours'] >= 0.2 * self.listUser['avg_hourplayed']) & (self.listUser['hours'] < 0.6 * self.listUser['avg_hourplayed']),
                    self.listUser['hours'] >= 0
                ]
            values = [5, 4, 3, 2, 1]
            self.listUser['rating'] = np.select(condition,values)

    def fit(self):
        self.PreProcessingCSV()
        if self.notTrain:
            self.CalAveragePlayedTime()
            self.CalRatingGame()
            self.CreateDataMatrix()

filename1 = "steam_user.csv"
test = dataProcessing(filename1)
test.fit()

