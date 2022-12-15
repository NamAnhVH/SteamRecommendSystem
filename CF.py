import dataProcessing as dp
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import scipy as sp

class CF(object):
    def __init__ (self,dataMatrix, k = 5):
        self.dataMatrix          = dataMatrix
        self.matrixTable         = None
        self.matrixTableSpare    = None
        self.gameSimilarity      = None
        self.userSimilarity      = None
        self.gameSimilarityTable = None
        self.userSimilarityTable = None

    def CreateMatrixTable(self):
        self.matrixTable = self.dataMatrix.pivot_table(index = ['userId'], columns = ['name'], values = 'rating')
        self.matrixTable = self.matrixTable.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)), axis=1)
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

    def PredictRating(self, u, i, k=0):
        self.CreateSimilarityTable()
        dataUserHaveGame = self.dataMatrix[(self.dataMatrix['name'] == i)]
        locationGame = self.dataMatrix[self.dataMatrix['name'] == i].index
        user_rated_i = []
        sim = []
        for line in range(len(dataUserHaveGame)):
            user_rated_i.append(dataUserHaveGame['userId'][locationGame[line]])
        for k in range(len(user_rated_i)):
            sim.append([user_rated_i[k],self.userSimilarityTable[u][user_rated_i[k]]])
        
        frametest = pd.DataFrame(sim, columns = ["user_rated_i","sim"])    
        # print(sim)
        # print(frametest)        

# datatest = [[1,1,5],[1,2,4],[1,3],[1,4,1],[1,5,1],
#             [2,1,5],[2,2,],[2,3,3],[2,4,1],[2,5,3],
#             [3,1,1],[3,2,],[3,3,1],[3,4,4],[3,5,5],
#             [4,1,3],[4,2,1],[4,3,],[4,4,5],[4,5,],
#             [5,1,2],[5,2,],[5,3,],[5,4,4],[5,5,],
#             [6,1,],[6,2,4],[6,3,1],[6,4,],[6,5,],
#             [7,1,],[7,2,],[7,3,1],[7,4,5],[7,5,4],
#             ]
# dataMatrix = pd.DataFrame(data = datatest, columns = ["userId","name","rating"])
# print(dataMatrix)
filename = "steam_user.csv"
test = dp.dataProcessing(filename)
# print(test.dataMatrix)
test.CreateDataMatrix()
cf = CF(test.dataMatrix)
cf.PredictRating(151603712,"Dota 2", 0)
cf.CreateSimilarityTable()
print(cf.userSimilarityTable)


