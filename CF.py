import dataProcessing as dp
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import scipy as sp

class CF(object):
    def __init__ (self, dataMatrix, listGame, notTrain = True, k = 50, top = 5):
        self.dataMatrix            = dataMatrix
        self.matrixTable           = None
        self.matrixTableSpare      = None
        self.gameSimilarity        = None
        self.userSimilarity        = None
        self.gameSimilarityTable   = None
        self.userSimilarityTable   = None
        self.k                     = k
        self.top                   = top
        self.listGame              = listGame
        self.notTrain              = notTrain
        self.listAverageUserRating = None

    def CreateMatrixTable(self):
        self.matrixTable = self.dataMatrix.pivot_table(index = ['userId'], columns = ['name'], values = 'rating')
        self.listAverageUserRating = self.matrixTable.apply(lambda x: np.mean(x),axis = 1)
        self.matrixTable = self.matrixTable.apply(lambda x: (x - np.mean(x)), axis=1)       
        self.matrixTable = self.matrixTable.fillna(0)
        self.matrixTable = self.matrixTable.T

    def CalSimilarity(self):        
        self.CreateMatrixTable()
        self.matrixTableSpare = sp.sparse.csr_matrix(self.matrixTable.values)
        self.gameSimilarity = cosine_similarity(self.matrixTableSpare)
        self.userSimilarity = cosine_similarity(self.matrixTableSpare.T)
    
    def CreateSimilarityTable(self):
        self.CalSimilarity()
        self.gameSimilarityTable = pd.DataFrame(self.gameSimilarity, index = self.matrixTable.index, columns = self.matrixTable.index)
        self.userSimilarityTable = pd.DataFrame(self.userSimilarity, index = self.matrixTable.columns, columns = self.matrixTable.columns)

    def PredictRating(self, u, i):
        user_rated_i = self.dataMatrix['userId'][self.dataMatrix['name'] == i].tolist()
        listUserSimilarityU = self.userSimilarityTable.loc[u][user_rated_i]
        listUserSimilarityU = listUserSimilarityU.sort_values(ascending = False).iloc[:self.k]
        # print(listUserSimilarityU)
        listIndex = listUserSimilarityU.index.to_series()
        dataRatedI = self.matrixTable.loc[i]
        dataRatedI = pd.Series(dataRatedI, index = listIndex , name = 'rate_point')
        dataRatedI = pd.concat([dataRatedI,listUserSimilarityU], axis=1)
        dataRatedI['total'] = dataRatedI['rate_point'] * dataRatedI[u]
        return np.sum(dataRatedI['total']) / (np.sum(abs(dataRatedI[u])) + 1e-8) + self.listAverageUserRating[u]
        # return np.sum(dataRatedI['total']) / (np.sum(abs(dataRatedI[u])) + 1e-8)
        
    def Recommend(self, u):
        locationUser = self.dataMatrix[self.dataMatrix['userId'] == int(u)].index
        items_rated_by_u = self.dataMatrix['name'].iloc[locationUser].tolist()
        def take_energy(power):
            return power['rating']
        game = {'game': None, 'rating': None}
        list_game = []
        listGame = self.listGame['name'].tolist()
        for i in range(len(listGame)):
            if listGame[i] not in items_rated_by_u:
                count = self.PredictRating(u, listGame[i])
                game['game'] = listGame[i]
                game['rating'] = count
                list_game.append(game.copy())
        sorted_game = sorted(list_game, key = take_energy, reverse = True)
        if self.notTrain:
            sorted_game = sorted_game[0:self.top]
            data = pd.DataFrame(sorted_game)
            return data
        else:
            data = pd.DataFrame(sorted_game)
            return self.RMSE(u,data,Input.dataMatrixTest)                  

    def RMSE(self, u, data, dataMatrixTest):
        if self.notTrain == False:
            SE = 0
            listGameTest = dataMatrixTest[dataMatrixTest['userId'] == u]
            location = listGameTest.index
            for i in range(len(listGameTest)):
                pred = data['rating'][data['game'] == listGameTest['name'][location[i]]].values
                SE += (pred - listGameTest['rating'][location[i]])**2

        ans = np.sqrt(SE/len(listGameTest))
        print(ans)
        return ans

# datatest = [[1,1,5],[1,2,4],[1,4,2],[1,5,2],
#             [2,1,5],[2,3,4],[2,4,2],[2,5,0],
#             [3,1,2],[3,3,1],[3,4,3],[3,5,4],
#             [4,1,0],[4,2,0],[4,4,4],
#             [5,1,1],[5,4,4],
#             [6,2,2],[6,3,1],
#             [7,3,1],[7,4,4],[7,5,5],
#             ]
# dataMatrix = pd.DataFrame(data = datatest, columns = ["userId","name","rating"])
# listGame = [1,2,3,4,5]
# listGame = pd.DataFrame(data = listGame, columns = ['name'] )
# cf = CF(dataMatrix,listGame,True,2)
# cf.CreateSimilarityTable()
# print(cf.Recommend(1))

filename = "steam_user.csv"
Input = dp.dataProcessing(filename,False)
Input.fit()
cf = CF(Input.dataMatrix,Input.listGame,Input.notTrain,15)
cf.CreateSimilarityTable()
# cf.Recommend(151603712)
# print(len(Input.listUserId))
ans = 0
for u in Input.listUserId:
    ans += cf.Recommend(u)
ans = ans/len(Input.listUserId)
print(1)
print(ans)
print(1)
# print(Input.dataMatrixTest[Input.dataMatrixTest['userId'] == 242937979])
# print(len(Input.dataMatrix))
# print(dataMatrix)
# print(cf.matrixTable)
# print(cf.userSimilarityTable)
# print(len(Input.listUserId))
# print(cf.average)



