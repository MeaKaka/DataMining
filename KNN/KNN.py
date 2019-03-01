# KNN数据有两类一类是训练数据,一类是待分类数据
# 训练数据是已确定类别的数据
# 计算待分类数据和每个已确定数据的距离,取其中最近的K个
# 则此待分类数据的类别为k个数据中出现次数最多的类别
import math
import collections

class KNN(object):
    def __init__(self,traindata,classVec,k):
        self.traindata = traindata #训练数据
        self.classVec = classVec # 训练数据对应的类别
        self.k = k

    # 计算测试数据和训练数据的距离曼哈顿距离
    def getDistance_Manhattan(self, testdata,data):
        distance = 0
        for i in range(len(data)):
            distance += abs(testdata[i] - data[i])
        return distance

    # 欧几里得距离
    def getDistance_Euclidean(self, testdata,data):
        distance = 0
        for i in range(len(data)):
            distance += pow(testdata[i] - data[i],2)
        return math.sqrt(distance)

    #  闵可夫斯基距离
    def getDistance_Minikowski(self, testdata,data):
        distance = 0
        for i in range(len(data)):
            newdistance = abs(testdata[i] - data[i])
            if newdistance>distance:
                distance = newdistance
        return distance

    def getClass(self,testdata):
        scoreList_Man = {}
        scoreList_Euc = {}
        scoreList_Min = {}
        for i in range(len(self.traindata)):
            scoreList_Man[i] = self.getDistance_Manhattan(testdata,self.traindata[i])
            scoreList_Euc[i] = self.getDistance_Euclidean(testdata,self.traindata[i])
            scoreList_Min[i] = self.getDistance_Minikowski(testdata,self.traindata[i])
        scoreList_Man = sorted(scoreList_Man.items(),key=lambda d : d[1],reverse=True)
        scoreList_Euc = sorted(scoreList_Euc.items(),key=lambda d : d[1],reverse=True)
        scoreList_Min = sorted(scoreList_Min.items(),key=lambda d : d[1],reverse=True)
        # print(scoreList_Man)
        candidateClass_Man = []
        candidateClass_Euc = []
        candidateClass_Min = []
        for i in range(self.k):
            candidateClass_Man.append(self.classVec[scoreList_Man[i][0]])
            candidateClass_Euc.append(self.classVec[scoreList_Euc[i][0]])
            candidateClass_Min.append(self.classVec[scoreList_Min[i][0]])
        candidateClass_Man.extend(candidateClass_Euc)
        candidateClass_Man.extend(candidateClass_Min)
        classCount = collections.Counter(candidateClass_Man)
        return classCount.most_common(1)[0][0]


if __name__=='__main__':
    traindata = [[1,2,3,4,2,1,3,3],
                 [3, 4, 3, 4, 2, 1, 4, 3],
                 [1, 2, 3, 3, 2, 1, 3, 1],
                 [2, 4, 1, 4, 2, 3, 3, 3],
                 [1, 2, 3, 3, 2, 1, 4, 3],
                 [1, 3, 3, 4, 2, 1, 3, 4]]
    # 训练样本对应的分类结果
    classVec = ['a', 'b', 'a', 'a', 'b', 'b']
    testdata = [1,2,4,4,2,1,1,3]
    k = 3
    KNN = KNN(traindata,classVec,k)
    print(KNN.getClass(testdata))
