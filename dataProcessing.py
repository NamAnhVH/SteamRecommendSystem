import pandas as pd
import numpy as np


class dataProcessing(object):
    def __init__ (self, listUserFile, listGameFile):
        self.listUserFile      = listUserFile
        self.listGameFile      = listGameFile
        self.dataGame          = None
        self.listNameGame      = None
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
        self.dataGame = pd.read_csv(self.listGameFile)
        self.listNameGame = self.dataGame.drop(
            columns = [
                        'appid','release_date', 'english', 'developer', 'publisher', 'platforms', 'required_age','categories', 'genres', 'steamspy_tags',
                        'achievements', 'positive_ratings', 'negative_ratings','average_playtime', 'median_playtime', 'owners', 'price'
                    ]
        )
        self.numberOfGame = len(self.listNameGame)
        self.dataUser = pd.read_csv(self.listUserFile)
        self.listUser = self.dataUser.drop(columns = ["0"])
        self.listUserId = self.listUser.drop(columns = ["name", "behavior", "hours"])
        self.listUserId = list(set(self.listUserId['userId'].values.tolist()))
        self.listBehavior = self.listUser.drop(columns = ["userId", "name", "hours"])
        self.numberOfUser = len(self.listUserId)
        self.listUserId = pd.DataFrame(data = self.listUserId, columns = ['userId'])
    
    def CreateDataMatrix(self):
        self.PreProcessingCSV()
        self.CalAveragePlayedTime()
        self.CalRatingGame()
        self.dataTable = self.listNameGame.merge(self.listUser, how = 'left', on = 'name')
        self.dataMatrix = self.dataTable.drop(columns = ["behavior","hours","avg_hourplayed"])
        self.listUser = self.listUser.drop(columns = ["avg_hourplayed","behavior"])


    def CalAveragePlayedTime(self):
        self.listUser = self.listUser[(self.listUser['behavior'] == 'play')]
        # print(self.listUser[(test.listUser['name'] == 'Rag Doll Kung Fu')])

        # self.listUser = self.listUser[self.listUser.groupby('name').userId.transform(len) >= 20]

        self.listUser['name'].nunique()

        self.listUser['name'] = self.listUser['name'].astype(str)

        self.averagePlayedTime = self.listUser.groupby(['name'], as_index = False).hours.mean()
        self.averagePlayedTime['avg_hourplayed'] = self.averagePlayedTime['hours']
        self.averagePlayedTime.drop(columns = 'hours', inplace = True)

        self.listUser = self.listUser.merge(self.averagePlayedTime, how = 'left', on = 'name')
        # print(self.listUser[(test.listUser['name'] == 'Rag Doll Kung Fu')])


        

    
    def CalRatingGame(self):
        condition = [
            self.listUser['hours'] >= (0.8 * self.listUser['avg_hourplayed']),
            (self.listUser['hours'] >= 0.6 * self.listUser['avg_hourplayed']) & (self.listUser['hours'] < 0.8*self.listUser['avg_hourplayed']),
            (self.listUser['hours'] >= 0.4 * self.listUser['avg_hourplayed']) & (self.listUser['hours'] < 0.6*self.listUser['avg_hourplayed']),
            (self.listUser['hours'] >= 0.2 * self.listUser['avg_hourplayed']) & (self.listUser['hours'] < 0.4*self.listUser['avg_hourplayed']),
             self.listUser['hours'] >= 0
        ]
        values = [5, 4, 3, 2, 1]
        self.listUser['rating'] = np.select(condition,values)

    # def CreateMatrixTable(self):
    #     self.CreateDataMatrix()
    #     self.matrixTable = self.dataMatrix.pivot_table(index = ['userId'], columns = ['name'], values = 'rating')    


filename = "steam.csv"
filename1 = "steam_user.csv"
test = dataProcessing(filename1, filename)
test.CreateDataMatrix()
# print(test.listUser)
# test.CreateMatrixTable()
# print(test.listUser[(test.listUser['name'] == 'Rag Doll Kung Fu')])
# print(test.listUser)
# print(test.dataUser[(test.dataUser['name'] == "Rag Doll Kung Fu")])
# print(test.numberOfGame)
# print(test.numberOfUser)
# print(test.listUserId)
# print(test.dataMatrix)