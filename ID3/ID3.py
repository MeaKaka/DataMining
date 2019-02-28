#目标: 基于已有数据构造决策树,同时能将测试数据分到正确的类别

# 读取数据
# 划分数据集
# 计算信息增益
# 寻找最佳特征划分数据集,可能是个多分类
# 递归依次确定最佳特征构树

import math
class ID3(object):
    def __init__(self,dataSet,labels):
        self.dataSet = dataSet
        self.labels = labels
        self.subdataSet = []
        self.chooseFeature = 0
        self.shannonEnt = 0.0

    # 计算信息墒更改self.shannonEnt的值
    def calcShannonEnt(self,data):
        num = len(data)
        # 统计label的个数
        labelCounts = {}
        for featVec in data:
            currentLabel = featVec[-1]
            if currentLabel not in labelCounts.keys():
                labelCounts.setdefault(currentLabel, 0)
            labelCounts[currentLabel] += 1
        # 计算信息熵
        shannonEnt = 0.0
        for key in labelCounts:
            prob = float(labelCounts[key]) / num
            shannonEnt += prob * math.log2(1 / prob)
        return shannonEnt

    # 按照最大信息增益 划分数据集
    # 定义按照某个特征进行划分的函数 splitDataSet
    # axis是选取的特征,value是对应的特征的值
    def splitDataSet(self, dataset, feature, value):
        retDataSet = []
        for featVec in dataset:
            if featVec[feature] == value:
                reduceFeatVec = featVec[:feature]
                reduceFeatVec.extend(featVec[feature + 1:])
                retDataSet.append(reduceFeatVec)
        return retDataSet  #返回不含划分特征的子集

    # 返回增益最大的特征的下标
    def chooseBestFeatureToSplit(self,data):
        numFeature = len(data[0]) - 1

        # 确认原始基础信息熵Entropy(S)
        baseEntropy = self.calcShannonEnt(data)
        bestInforGain = 0
        bestInforGainRatio = 0
        bestFeature = -1
        # 对每一个特征都进行讨论
        for i in range(numFeature):
            featList = [number[i] for number in data]
            # print(featList)
            uniqualVals = set(featList)
            newEntrogy = 0
            SplitInfo = 0
            #求EntropyA(S)值
            # P1AEntropy(S1)+...+PnAEntropy(Sn)
            for value in uniqualVals:
                prob = len(self.splitDataSet(data, i, value)) / float(len(data)) #即Pi
                SplitInfo += prob * math.log2(1 / prob) # 计算内在信息
                newEntrogy += prob * self.calcShannonEnt(self.subdataSet)
            # 计算增益Gain(S, A) = Entropy(S)−EntropyA(S)
            infoGain = baseEntropy - newEntrogy
            # 比较得到最大增益
            if infoGain > bestInforGain:
                bestInforGain = infoGain
                bestFeature = i

            # C4.5 将将信息增益改为信息增益比IGR = Gain/H. H表示内在信息，内在信息可以看作是整体取值。比如说天气A和活动与否S，计算Entropy_A(S) 应该考虑不同天气对应活动与否的情况，而H则只需要考虑天气A这一属性内部取值的情况。引入这一变量，会出现当一个属性本身不确定性较大时，被选择的概率也就不高的情况。
            # 计算增益比, 获取最大增益比
            infoGainRatio = infoGain / SplitInfo
            if infoGainRatio > bestInforGainRatio:
                bestInforGainRatio = infoGainRatio
                bestFeature = i

        return bestFeature



    # 选取占比最多的类别
    def majorityCnt(self,classList):
        classCount = {}
        for vote in classList:
            if vote not in classCount.keys():
                classCount.setdefault(vote, 0)
            classCount[vote] += 1
        sortedClassCount = sorted(classCount.items(), key=lambda i:i[1], reverse=True)
        return sortedClassCount[0][0]

    # 递归构造ID3树
    def createTree(self,dataSet, labels):
        classList = [example[-1] for example in dataSet]
        # 类别相同，停止划分
        if classList.count(classList[0]) == len(classList):
            return classList[0]
        # 判断是否遍历完所有的特征,是，返回个数最多的类别
        if len(dataSet[0]) == 1:
            return self.majorityCnt(classList)
        #按照信息增益最高选择分类特征属性
        bestFeature = self.chooseBestFeatureToSplit(dataSet) #分类编号
        bestFeatureLabel = labels[bestFeature]  #该特征的label
        myTree = {bestFeatureLabel: {}}
        del (labels[bestFeature]) #移除该label
        featureValues = [data[bestFeature] for data in dataSet]
        uniqueVals = set(featureValues)
        for value in uniqueVals:
            subLabels = labels[:]  #子集合
            #构建数据的子集合，并进行递归
            myTree[bestFeatureLabel][value] = self.createTree(self.splitDataSet(dataSet, bestFeature, value), subLabels)
        return myTree

    # 运用决策树通过递归进行分类，一层层的解析树
    def classify(self,inputTree, featureLabels, test):
        firstStr = list(inputTree.keys())[0] #树的第一个属性
        secondeDict = inputTree[firstStr]
        print(featureLabels)
        print(firstStr)
        print("sendDict")
        print(secondeDict)
        featureIndex = featureLabels.index(firstStr)
        print(featureIndex)
        classLabel = None
        for key in secondeDict.keys():
            if test[featureIndex] == key:
                if type(secondeDict[key]).__name__ == 'dict':
                    classLabel = self.classify(secondeDict[key], featureLabels, test)
                else:
                    classLabel = secondeDict[key]
        return classLabel

if __name__ == '__main__':
    dataSet = [["U", 2, 'win'], ["T", 1, 'win'], ['U', 1, 'lose'], ['U', 2, 'win'], ['T', 2, 'lose']]
    labels = ['team', 'rank']
    A = ID3 (dataSet,labels)
    Tree = A.createTree(dataSet, labels)
    # print(Tree)
    labels = ['team', 'rank'] #需注意之前的labels在建树的过程中被更改了因此需要对labels进行重新定义
    print(A.classify(Tree, labels, ["U", 2]))
