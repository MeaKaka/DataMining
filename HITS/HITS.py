# 获取链接关系,确定hub,Authority集合
# 更新hub,authority值

from pygraph.classes.digraph import digraph

import math

def HITS(G):
    total = 0
    # 更新authority的值
    for node in G.nodes():
       authority[node] = 0
       for incident in G.incidents(node):
           print(authority[node])
           print(incident)
           # print(hub[incident])
           authority[node] = authority[node] + hub[incident]
       total = total + pow(authority[node],2)
    total = math.sqrt(total)
    # 对每个页面的authority进行规范化处理
    for node in G.nodes():
        authority[node] = authority[node]/total
    # 对hub的值进行相同的处理
    total = 0
    for node in G.nodes():
       hub[node] = 0
       for neighbor in G.neighbors(node):
           hub[node] = hub[node] + authority[neighbor]
       total = total + pow(hub[node],2)
    total = math.sqrt(total)
    for node in G.nodes():
        hub[node] = hub[node]/total
    return authority,hub




if __name__ == '__main__':
    # G = nx.DiGraph()
    G = digraph()
    G.add_nodes(["A", "B", "C", "D", "E"])
    G.add_edge(("A", "C"))
    G.add_edge(("A", "D"))
    G.add_edge(("B", "D"))
    G.add_edge(("C", "E"))
    G.add_edge(("D", "E"))
    G.add_edge(("B", "E"))
    G.add_edge(("E", "A"))
    hub = {"A":1,"B":1,"C":1,"D":1,"E":1}
    authority = {"A":1,"B":1,"C":1,"D":1,"E":1}
    e = 0.00005
    newauthority,newhub = HITS(G)
    E = min(list(authority.values())) - min(list(newauthority.values()))
    E = min(E,min(list(hub.values())) - min(list(newhub.values())))
    while  abs(E)>e:
        authority = newauthority
        hub = newhub
        newauthority,newhub = HITS(G)
        E = list(authority.values()) - list(newauthority.values())
        E.extend(list(hub.values()) - list(newhub.values()))
    print(hub,authority)