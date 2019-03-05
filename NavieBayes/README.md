### NaiveBayes
垃圾邮件分类/用户评价情感分析
假设输入的不同特征之间是独立的。
给定一个类，每个属性属于此类的概率独立于其他属性。<br>
贝叶斯中的属性有出现与不出现两种状态

##### 代码


```math
P(y_i|x)=\frac{P(x|y_i)P(y_i)}{P(x)}
```
对每一个类型yi都要计算每一个特征xj的条件概率，

```math
P(y_i|x)=\frac{P(x|y_i)P(y_i)}{P(x)}= \frac{P(y_i)}{P(x)}\prod_{j=0}^{n}P(x_j|y_i)
```
这时候一般用矩阵进行计算，能得到每个特征和每个类型之间的对应关系。将结果转化为log运算后便于将求积运算转化为求和运算。
```
    <!-- 利用训练数据得到概率矩阵-->
    def trainNB(self,Vec):
        numTrain = len(Vec)
        numWords = len(Vec[0])
        classSet = list(set(self.classVec))
        for classN in classSet:
            self.baseP.append(self.classVec.count(classN)/float(numTrain))
    
        <!--防止某个类别计算出的概率为0，导致最后相乘都为0，使用拉普拉斯修正-->
        pNum = []
        pDenom = []
        for i in range(self.classNum):
            pNum.append(np.ones(numWords))
            pDenom.append(2)
        for i in range(numTrain):
            for j in range(self.classNum):
                if classVec[i] == classSet[j]:
                    <!--将classSet[j]类下的每一个属性出现值对应加一-->
                    pNum[j] += Vec[i]
                    <!--sum(Vec[i])是在计算分到classSet[j]下的句子的长度,即当前循环classSet[j]出现的次数-->
                    pDenom[j] += sum(Vec[i])
    
    
        <!--这里使用log函数，方便计算,将后续的相乘问题更改为求和问题-->
        for i in range(self.classNum):
            self.pVect.append(np.log(pNum[i] / pDenom[i]))
```


```
    <!-- 将test数据与训练矩阵相乘 -->
    def classifyTest(self,testVec):
        p =float("-inf")
        location = 0
        for i in range(self.classNum):
            <!--预测过程，利用极大似然估计-->
            pN = sum(testVec*self.pVect[i])+np.log(self.baseP[i])
            if pN > p:
                p = pN
                location = i
            print(pN)
        return location
```
##### 对比高斯判别
高斯判别中x是连续的，而贝叶斯判别中x是离散的。
