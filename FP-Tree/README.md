### FP-Tree
频繁模式树算法(FrequentPattern Tree),避免了产生多个候选集.<br>
而FP-Tree算法则是发现频繁模式而不产生候选集.
Apriori在每次连接后都需要重新扫描数据,统计出现的频率,I/O消耗较大.
###### 算法步骤
1. 生成一项频繁集,降序排列,删除不符合支持度条件的组成项表头
2. 对原始数据的每一行数据删除非项表头数据,并进行降序排列
3. **生成FP-Tree**
    - 根节点为null
    - 依次读入排好序的每一行数据
    - 排名靠前的是祖先节点,靠后的是子孙节点
    - 如果有共同祖先,对应的公用祖先节点计数加一
4. 获取针对于每个节点的条件模式基,从根节点开始,向下回溯,不满足最小支持度的节点及子树不予考虑

###### 对比Apriori
两个算法的核心是一样的,确定每个属性的出现频率,确定组合属性的出现频率. FP-Tree是根据每一个组合数据去确定属性关系和属性频率,而Apriori是根据属性先行组合再从数据中确定频率.

###### 编码过程
核心在于FP-Tree的构造
python多叉树的构造和遍历：
