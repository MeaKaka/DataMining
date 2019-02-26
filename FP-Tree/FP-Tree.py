# 核心在于生成FP-Tree树
# 生成频繁一项集的代码可以与Apriori复用

class TreeNode(object):
    def __init__(self,value):
        self.val = value
        self.children = []
        self.num = 1

class FP_Tree(object):
    def __init__(self,itemSet,minSupport):
        self.minsupport = minSupport
        self.itemSet = itemSet
        self.candidate = {}
        self.FPTree = TreeNode('root')

    # 首先要对输入的set里的每一个元素有序化,以便进行后续的连接
    def _setOrder(self):
        message = []
        for item in self.itemSet:
            item.sort()
            message.append(item)
        self.itemSet = message

    # 生成频繁一项集
    def _candidate_1(self):
        for item in self.itemSet:
          for element in item:
              self.candidate[element]=0
        for item in self.itemSet:
          for element in item:
              self.candidate[element] = self.candidate[element]+1
        #

    #剪枝函数
    def _cut(self):
        for element in list(self.candidate):
            if self.candidate[element] < self.minsupport:
                del self.candidate[element]

    # 针对itemSet中的每一条元素删除频繁一项集中没有的,并对itemSet中的每一条元素依据一项集频繁程度排序
    def modifyItemset(self):
        # 剪枝后的self.candidate
        self._candidate_1()
        self._cut()
        # candidate = sorted(self.candidate,key= lambda candidate:self.candidate[1])  #key通过value的值进行排序
        candidateSet = list(self.candidate.keys())  # key的list集合
        candidateSet.sort(reverse=True) # 按降序排列
        # m = sorted(dic.iteritems(), key=lambda d: d[1], reverse=False)

        # 将非频繁一项集的元素删除,并对原始数据进行降序排列
        # print(candidateSet)
        for item in self.itemSet:
            for i in item:
                if i not in candidateSet:
                    item.remove(i)
        newitem = []
        for item in self.itemSet:
            if item == []:
                self.itemSet.remove(item)
            else:
                new = []
                for i in candidateSet:
                    # 利用查找的方式进行排序
                    if i in item:
                        new.append(i)
                newitem.append(new)
        self.itemSet = newitem
        # print(self.itemSet)

    # 构造FP-Tree
    def createFP_Tree(self):
        self.modifyItemset()
        # print(self.itemSet)
        for item in self.itemSet:
            # print(item)
            itemTree = self.FPTree
            # print(itemTree.val)
            for i in range(len(item)):
                childrenValue = []
                for j in range(len(itemTree.children)):
                    childrenValue.append(itemTree.children[j].val)
                if item[i] in childrenValue:
                    loc = childrenValue.index(item[i])
                    itemTree = itemTree.children[loc]
                    itemTree.num = itemTree.num +1
                    # print("in")
                else:
                    itemTree.children.append(TreeNode(item[i]))
                    itemTree = itemTree.children[-1]
                    # print("out")
            # print("end_______")

    # 用递归来生成合适的序列
    def getCandidate(self,node,candidatset):
        candidatset.append(node.val)
        childrenSet = node.children
        print(childrenSet)
        for item in childrenSet:
            print(item.val)
            print(item.num)
            if item.num >= self.minsupport:
                self.getCandidate(item,candidatset)
        return candidatset


    # 遍历FP_Tree得到符合条件的匹配
    def getCandidateList(self):
        self.createFP_Tree()
        itemTree = self.FPTree.children  # list
        candidateSet = []
        for item in itemTree:
            print(item.val)
            print(item.num)
            if item.num >= self.minsupport:
                candidateSet.append(self.getCandidate(item,[]))
                print(candidateSet)
        return candidateSet







Alist = [['1','3','4'],['2','3','5'],['1','2','3','5'],['2','5']]
A = FP_Tree(Alist,2)
A.getCandidateList()