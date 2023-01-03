import dataProcessing as dp
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import scipy as sp

class CF(object):
    def __init__ (self, dataMatrix, listUserId, listGame, uu = 1, notTrain = True, k = 50, top = 5):
        self.dataMatrix            = dataMatrix
        self.matrixTable           = None
        self.matrixTableSpare      = None
        self.Similarity            = None
        self.SimilarityTable       = None
        self.k                     = k
        self.top                   = top
        self.listGame              = listGame
        self.listUserId            = listUserId
        self.notTrain              = notTrain
        self.listAverageUserRating = None
        self.listAverageItemRating = None
        self.uu                    = uu

    def CreateMatrixTable(self):
        if self.uu:
            self.matrixTable = self.dataMatrix.pivot_table(index = ['userId'], columns = ['name'], values = 'rating')
            self.listAverageUserRating = self.matrixTable.apply(lambda x: np.mean(x), axis = 1)
            self.matrixTable = self.matrixTable.apply(lambda x: (x - np.mean(x)), axis=1)       
            self.matrixTable = self.matrixTable.fillna(0)
            self.matrixTable = self.matrixTable.T
        else:
            self.matrixTable = self.dataMatrix.pivot_table(index = ['name'], columns = ['userId'], values = 'rating')
            self.listAverageItemRating = self.matrixTable.apply(lambda x: np.mean(x), axis = 1)
            self.matrixTable = self.matrixTable.apply(lambda x: (x - np.mean(x)), axis=1)       
            self.matrixTable = self.matrixTable.fillna(0)
            self.matrixTable = self.matrixTable.T

    def CalSimilarity(self):        
        self.CreateMatrixTable()
        self.matrixTableSpare = sp.sparse.csr_matrix(self.matrixTable.values)
        self.Similarity = cosine_similarity(self.matrixTableSpare.T)

    def CreateSimilarityTable(self):
        self.CalSimilarity()
        self.SimilarityTable = pd.DataFrame(self.Similarity, index = self.matrixTable.columns, columns = self.matrixTable.columns)

    def PredictRating(self, u, i):
        if self.uu:
            user_rated_i = self.dataMatrix['userId'][self.dataMatrix['name'] == i].tolist()
            listUserSimilarityU = self.SimilarityTable.loc[u][user_rated_i]
            listUserSimilarityU = listUserSimilarityU.sort_values(ascending = False).iloc[:self.k]
            listIndex = listUserSimilarityU.index.to_series()
            dataRatedI = self.matrixTable.loc[i]
            dataRatedI = pd.Series(dataRatedI, index = listIndex , name = 'rate_point')
            dataRatedI = pd.concat([dataRatedI,listUserSimilarityU], axis=1)
            dataRatedI['total'] = dataRatedI['rate_point'] * dataRatedI[u]
            return np.sum(dataRatedI['total']) / (np.sum(abs(dataRatedI[u])) + 1e-8) + self.listAverageUserRating[u]
        else:
            item_rated_by_u = self.dataMatrix['name'][self.dataMatrix['userId'] == int(u)].tolist()
            listItemSimilarityI = self.SimilarityTable.loc[i][item_rated_by_u]
            listItemSimilarityI = listItemSimilarityI.sort_values(ascending = False).iloc[:self.k]
            listIndex = listItemSimilarityI.index.to_series()
            dataRatedByU = self.matrixTable.loc[u]
            dataRatedByU = pd.Series(dataRatedByU, index = listIndex, name = 'rate_point')
            dataRatedByU = pd.concat([dataRatedByU,listItemSimilarityI], axis = 1)
            dataRatedByU['total'] = dataRatedByU['rate_point'] * dataRatedByU[i]
            return np.sum(dataRatedByU['total']) / (np.sum(abs(dataRatedByU[i])) + 1e-8) + self.listAverageItemRating[i]
        
    def Recommend(self, u):
        def take_energy(power):
                return power['rating']
        game = {'game': None, 'rating': None}
        list_game = []
        listGame = self.listGame['name'].tolist()
        locationUser = self.dataMatrix[self.dataMatrix['userId'] == int(u)].index
        items_rated_by_u = self.dataMatrix['name'].iloc[locationUser].tolist()
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



# filename = "steam_user.csv"
# Input = dp.dataProcessing(filename,False)
# Input.fit()
# cf = CF(Input.dataMatrix,Input.dataUserId,Input.dataGame,0,Input.notTrain,100)
# cf.CreateSimilarityTable()
# print(cf.Recommend(151603712)) 
# # print(len(Input.listUserId))

# ans = 0
# for u in Input.listUserId:  
#     ans += cf.Recommend(u)
# ans = ans/len(Input.listUserId)
# print(ans)

# datatest = [[1,1,5],[1,2,4],[1,4,2],[1,5,2],
#             [2,1,5],[2,3,4],[2,4,2],[2,5,0],
#             [3,1,2],[3,3,1],[3,4,3],[3,5,4],
#             [4,1,0],[4,2,0],[4,4,4],
#             [5,1,1],[5,4,4],
#             [6,2,2],[6,3,1],
#             [7,3,1],[7,4,4],[7,5,5],
#             ]
# datatest = [[1,1,5],[1,2,4],[1,4,1],[1,5,1],
#             [2,1,5],[2,3,3],[2,4,1],[2,5,3],
#             [3,1,1],[3,3,1],[3,4,4],[3,5,5],
#             [4,1,3],[4,2,1],[4,4,5],
#             [5,1,2],[5,4,4],
#             [6,2,4],[6,3,1],
#             [7,3,1],[7,4,5],[7,5,4],
#             ]
# dataMatrix = pd.DataFrame(data = datatest, columns = ["userId","name","rating"])
# listGame = [1,2,3,4,5]
# listUserId = [1,2,3,4,5,6,7]
# listGame = pd.DataFrame(data = listGame, columns = ['name'] )
# listUserId = pd.DataFrame(data = listUserId, columns = ['userId'])
# cf = CF(dataMatrix,listUserId,listGame,1,True,2)
# cf.CreateSimilarityTable()
# print(cf.Recommend(2))




