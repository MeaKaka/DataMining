# 实现朴素贝叶斯的关键是计算不同类下的不同特征的概率

# _*_ coding:utf-8 _*_
import numpy as np

class NaiveBayes(object):
    def __init__(self,postingList,classVec,classNum):
        self.vocab = []
        self.postingList = postingList
        self.classVec = classVec
        self.baseP = []
        self.pVect = []
        self.classNum =classNum
    # 创建词库
    def createVocabList(self,dataSet):
        vocabSet = set([])
        for document in dataSet:
            # 求并集
            vocabSet = vocabSet | set(document)
        self.vocab = list(vocabSet)

    # 将文本转化为向量的形式
    def setOfWords2Vec(self, inputSet):
        Vec = [0] * len(self.vocab)
        for word in inputSet:
            if word in self.vocab:
                Vec[self.vocab.index(word)] = 1
            else:
                print("The lib has no such word")
        return Vec


    def trainNB(self,Vec):
        numTrain = len(Vec)
        numWords = len(Vec[0])
        classSet = list(set(self.classVec))
        for classN in classSet:
            self.baseP.append(self.classVec.count(classN)/float(numTrain))

        #防止某个类别计算出的概率为0，导致最后相乘都为0，使用拉普拉斯修正
        pNum = []
        pDenom = []
        for i in range(self.classNum):
            pNum.append(np.ones(numWords))
            pDenom.append(2)
        for i in range(numTrain):
            for j in range(self.classNum):
                if classVec[i] == classSet[j]:
                    # 将classSet[j]类下的每一个属性出现值对应加一
                    pNum[j] += Vec[i]
                    # sum(Vec[i])是在计算分到classSet[j]下的句子的长度,即当前循环classSet[j]出现的次数
                    pDenom[j] += sum(Vec[i])


        # 这里使用log函数，方便计算,将后续的相乘问题更改为求和问题
        for i in range(self.classNum):
            self.pVect.append(np.log(pNum[i] / pDenom[i]))

    def classifyTest(self,testVec):
        p =float("-inf")
        location = 0
        for i in range(self.classNum):
            pN = sum(testVec*self.pVect[i])+np.log(self.baseP[i])
            if pN > p:
                p = pN
                location = i
            print(pN)
        return location

    def testingNB(self,testEntry):
        trainMat=[]
        self.createVocabList(self.postingList)
        for postinDoc in self.postingList:
            trainMat.append(self.setOfWords2Vec(postinDoc))
        self.trainNB(np.array(trainMat))
        testVec = np.array(self.setOfWords2Vec(testEntry))
        print(testEntry,'classified as: ',self.classifyTest(testVec))


if __name__=='__main__':
    # 设置训练样本
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    # 训练样本对应的分类结果
    classVec = [2, 1, 0, 2, 0, 1]
    # 分类个数
    classNum = 3
    NaiBayes = NaiveBayes(postingList,classVec,classNum)
    # 测试数据
    NaiBayes.testingNB(["my","garbage"])
