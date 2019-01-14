# 将整个pagerank过程分为两步,一是构造概率转移矩阵;二是更新特征向量的值
# 特征向量的值可以看作是每个页面的PR值,初始PR值为均值,即初始选择概率相同
# 页面的跳转过程可以看作是一个马氏链,迭代求PR的过程可以看作是求平稳分布

import numpy as np
# 邻接矩阵
G = [
    [0,1,1,0,0,1,0] ,
    [1,1,0,0,1,0,1],
    [0,0,1,0,0,0,0],
    [0,1,1,1,0,1,0],
    [1,0,1,0,0,1,1],
    [0,0,1,1,0,0,1],
    [1,0,1,0,1,1,0]
    ]
# 设置阻尼系数
a = 0.85
# 初始化随机过程
e = np.ones(7)
damping = [[i*1/7] for i in e ]
# 将邻接矩阵更新为概率转移矩阵,
def probabilityMatrix (G):
    Gm = []
    for i in range(len(G)):
        total = 0
        for j in range(len(G[i])):
            if G[i][j] != 0:
                total = total + G[i][j]
        tran_prob = 1 / total
        Gm_tmp = []
        for j in range(len(G[i])):
            Gm_tmp.append(tran_prob * G[i][j])
        Gm.append(Gm_tmp)
    Gm = np.transpose(Gm)
    return Gm

# 考虑阻尼系数,由邻接矩阵更新特征向量的值
def PageRank(Gm,a,v):
    vk = np.dot(Gm,v)
    vk = np.dot(a,vk)+np.dot((1-a),damping)
    return vk


if __name__ == '__main__':
    v = damping
    Gm = probabilityMatrix(G)
    # print(Gm)
    # print(v)
    e = 0.000005
    v1 = PageRank(Gm,a,v)
    E = v1-v
    i =0
    while  abs(E.any())>e:
        v = v1
        v1 = PageRank(Gm,a,v)
        E = v1-v
        i = i+1
        print("第%s次迭代" %i)
    print(v1)
