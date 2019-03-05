### KNN
KNN算法全名为k-Nearest Neighbor，就是K最近邻的意思
###### 求距离的方式
- 曼哈顿距离

```math
L(x_i,j_i)=\sum_{l=1}^{n}{|x_i^{(l)}-y_i^{(l)}|}
```
- 欧式距离
```math
L(x_i,j_i)=(\sum_{l=1}^{n}{|x_i^{(l)}-y_i^{(l)}|^2})^{\frac{1}{2}}
```
- 闵可夫斯基距离
```math
L(x_i,j_i)=\max{|x_i^{(l)}-y_i^{(l)}|}
```
###### 编码过程
关键是找出距离前k个最小值，并获取到他们的位置下标

```
<!--用字典存储，key为下标，value表示距离-->
<!--利用sorted函数指定排序依据和排序顺序-->
scoreList_Man = sorted(scoreList_Man.items(),key=lambda d : d[1],reverse=True)
```
获取下标后，找到下标对应的类别，统计每个类别出现的次数

```
<!--使用collections.Counter类进行计数-->
classCount = collections.Counter(candidateClassList)
<!--k表示出现次数最多的K个类别-->
<!--返回的是(类别,次数)的list-->
classCount.most_common(k)

```
###### 注意
- 如果直接使用KNN的话，我们会发现，三个维度上的数据相差过大，即前两个维度对于“距离”的影响要比第三个维度大得多。为了解决这个问题，我们要对数据进行预处理：归一化。
- 噪声剔除

###### 对比kNN与K-means
一个是分类算法一个是聚类算法
