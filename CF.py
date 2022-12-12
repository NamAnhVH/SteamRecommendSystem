import dataProcessing as dp
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import scipy as sp

class CF(object):
    def __init__ (self, numberOfUser, numberOfGame, dataMatrix, k = 5):
        self.dataMatrix          = dataMatrix
        self.numberOfUser        = numberOfUser
        self.numberOfGame        = numberOfGame
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
        self.matrixTable = self.matrixTable.loc[:, (self.matrixTable != 0).any(axis = 0)]

    def CalSimilarity(self):        
        self.CreateMatrixTable()
        self.matrixTableSpare = sp.sparse.csr_matrix(self.matrixTable.values)
        self.gameSimilarity = cosine_similarity(self.matrixTableSpare)
        self.userSimilarity = cosine_similarity(self.matrixTableSpare.T)
    
    def CreateSimilarityTable(self):
        self.CalSimilarity()
        self.gameSimilarityTable = pd.DataFrame(self.gameSimilarity, index = self.matrixTable.index, columns = self.matrixTable.index)
        self.userSimilarityTable = pd.DataFrame(self.userSimilarity, index = self.matrixTable.columns, columns=self.matrixTable.columns)

    # def PredictRating(self):
        

cf = CF(dp.test.numberOfUser,dp.test.numberOfGame,dp.test.dataMatrix)
cf.CreateSimilarityTable()
print(cf.gameSimilarityTable)

