# 设定数字k，从n个初始数据中随机的设置k个点为聚类中心点。
# 针对n个点的每个数据点，遍历计算到k个聚类中心点的距离，最后按照离哪个中心点最近，就划分到那个类别中。
# 对每个已经划分好类别的n个点，对同个类别的点求均值，作为此类别新的中心点。
# 循环直到最终中心点收敛。

import random

class Kmeans(object):
    def __init__(self,dataSet,k,):
        self.dataSet = dataSet
        self.k = k
        self.points = []  #记录当前聚类的中心点
        self.means = []  #记录当前聚类的情况
        self.result = {}

    # 选取k个随机点作为聚类中心点
    def getKpoints(self):
        self.points = random.sample(self.dataSet,self.k)
        # print(self.points)

    # 计算输入点与每一个类中心的欧式距离,得到分类值
    def getClassification (self,data):
        pointdistance = float("inf")
        j = 0
        location = 0
        for point in self.points:
            newpointdistance = 0
            for i in range(len(data)):
                newpointdistance += pow(point[i] - data[i], 2)
            if newpointdistance < pointdistance:
                location = j
                pointdistance = newpointdistance
            j = j+1
        return location

    # 将dataSet里的data都进行分类值的获取,并将相同分类值的data放到同一list中
    def getCategorylist(self):
        result = {}
        for data in self.dataSet:
            setnum = self.getClassification(data)
            result.setdefault(setnum,[])
            result[setnum].append(data)
        self.result = result

    # 计算被分到同一类别的数据的平均值,即更新聚类中心
    def updatePoints(self,resultList):
        self.points = []
        for result in resultList:
            average = [0 for i in range(len(resultList[result][0]))]
            for data in resultList[result]:
                # print(average)
                for i in range(len(data)):
                    average[i] = average[i] + data[i]
            for i in range(len(resultList[result][0])):
                average[i] = average[i]/len(resultList[result])
            self.points.append(average)

    # 返回聚类中心和聚类情况
    def loopIteration(self):
        oldpoint = self.getKpoints()
        self.getCategorylist()
        self.updatePoints(self.result)
        while not self.points == oldpoint:
            oldpoint = self.points
            self.getCategorylist()
            self.updatePoints(self.result)
        print(self.result)
        print(self.points)
        return self.points,self.result


if __name__ == '__main__':
    datalist = [(3,4),(5,6),(3,5),(4,6),(10,9),(12,3),(6,9),(2,7),(7,2)]
    Kmeans = Kmeans(datalist,3)
    Kmeans.loopIteration()
