import pandas as pd
import numpy as np


class dataProcessing(object):
    def __init__ (self, listUserFile):
        self.listUserFile      = listUserFile
        # self.listGameFile      = listGameFile
        self.dataGame          = None
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

    def PreProcessingCSV(self):
        # self.dataGame = pd.read_csv(self.listGameFile)
        # self.listNameGame = self.dataGame.drop(
        #     columns = [
        #                 'appid','release_date', 'english', 'developer', 'publisher', 'platforms', 'required_age','categories', 'genres', 'steamspy_tags',
        #                 'achievements', 'positive_ratings', 'negative_ratings','average_playtime', 'median_playtime', 'owners', 'price'
        #             ]
        # )
        # self.numberOfGame = len(self.listNameGame)
        self.dataUser = pd.read_csv(self.listUserFile)
        self.listUser = self.dataUser.drop(columns = ["0"])
        self.listUser = self.listUser[(self.listUser['behavior'] == 'play')]
        self.listUser = self.listUser[self.listUser.groupby('name').userId.transform(len) >= 10]
        self.listGame = list(set(self.listUser['name'].values.tolist()))
        self.listGame = pd.DataFrame(data = self.listGame, columns = ['name'])
        self.numberOfGame = len(self.listGame)
        self.listUserId = self.listUser.drop(columns = ["name", "behavior", "hours"])
        self.listUserId = list(set(self.listUserId['userId'].values.tolist()))
        self.listUserId = pd.DataFrame(data = self.listUserId, columns = ['userId'])
        self.numberOfUser = len(self.listUserId)
        self.listBehavior = self.listUser.drop(columns = ["userId", "name", "hours"])

    
    def CreateDataMatrix(self):
        self.PreProcessingCSV()
        self.CalAveragePlayedTime()
        self.CalRatingGame()
        self.dataTable = self.listGame.merge(self.listUser, how = 'left', on = 'name')
        self.dataMatrix = self.dataTable.drop(columns = ["behavior","hours","avg_hourplayed"])
        self.dataMatrix = self.dataMatrix[(self.dataMatrix["userId"].notnull())]
        self.listUser = self.listUser.drop(columns = ["behavior"])
        # print(self.dataMatrix)


    def CalAveragePlayedTime(self):
        self.listUser['name'].nunique()
        self.listUser['name'] = self.listUser['name'].astype(str)
        self.averagePlayedTime = self.listUser.groupby(['name'], as_index = False).hours.mean()
        self.averagePlayedTime['avg_hourplayed'] = self.averagePlayedTime['hours']
        self.averagePlayedTime.drop(columns = 'hours', inplace = True)
        self.listUser = self.listUser.merge(self.averagePlayedTime, how = 'left', on = 'name')

    def CalRatingGame(self):
        condition = [
            self.listUser['hours'] >= (0.8 * self.listUser['avg_hourplayed']),
            (self.listUser['hours'] >= 0.6 * self.listUser['avg_hourplayed']) & (self.listUser['hours'] < 0.8 * self.listUser['avg_hourplayed']),
            (self.listUser['hours'] >= 0.4 * self.listUser['avg_hourplayed']) & (self.listUser['hours'] < 0.6 * self.listUser['avg_hourplayed']),
            (self.listUser['hours'] >= 0.2 * self.listUser['avg_hourplayed']) & (self.listUser['hours'] < 0.4 * self.listUser['avg_hourplayed']),
             self.listUser['hours'] >= 0
        ]
        values = [5, 4, 3, 2, 1]
        self.listUser['rating'] = np.select(condition,values)

filename1 = "steam_user.csv"
test = dataProcessing(filename1)
test.CreateDataMatrix()
# print(test.dataMatrix)
# print(test.dataMatrix[test.dataMatrix['name'] == "Dota 2"])
# print(test.listUser)