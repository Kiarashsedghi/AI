from Library import *

class Main:
    def __init__(self):
        self.mazeMap=list()
        self.startPoint=None
        self.endPoint=None
        self.nodeCount=0
        self.pathCost=0
        self.pathExist=False
        self.pathActions=list()
        self.cutOffValue=90
        self.cutOffOccurred=False
        self.finalDepth=0
        self.maxDepth=1000


    def init_map(self):
        fh=open("./MAZE MAP")
        # row[:-1] for eliminating line feed
        self.mazeMap=[row[:-1] for row in  fh.readlines()]
        fh.close()
        for i in range(20):
            if "S" in self.mazeMap[i]:
                self.startPoint=(i,(self.mazeMap[i].index("S")))
            if "G" in self.mazeMap[i]:
                self.endPoint=(i,(self.mazeMap[i].index("G")))

    def goal_test(self,node):
        if node.state==self.endPoint:
            return 1
        return 0




    def report(self,algorithm):
        if self.pathExist is False:
            print("No path to goal :(")
            print("#Node created: ",self.nodeCount)
        else:
            print("#Node created: ",self.nodeCount)
            print("Path cost is: ",self.pathCost)
            if algorithm=="RDS":
                print("Depth: ",self.finalDepth)
            #TODO‌ path_print


    def bfs_go(self):
        '''
        This function performs BFS search
        :return:
        '''
        rootNode=GraphNode(self.startPoint,None,None,0)
        self.nodeCount+=1

        if self.goal_test(rootNode):
                return 1
        frontier=Queue()
        frontier.enqueue(rootNode)
        explored=list()

        while(1):
            if frontier.isempty():
                return 0
            node=frontier.dequeue()
            explored.append(node.state)

            for action in get_actions(self.mazeMap,node.state):
                childState=None
                if action=="right":
                    childState=(node.state[0],node.state[1]+2)
                elif action=="left":
                    childState=(node.state[0],node.state[1]-2)
                elif action=="up":
                    childState=(node.state[0]-1,node.state[1])
                elif action=="down":
                    childState=(node.state[0]+1,node.state[1])

                childNode=GraphNode(childState,node,action,node.cost+1)
                self.nodeCount+=1
                if (frontier.state_exist(childNode.state)) or (childNode.state not in explored):
                    if self.goal_test(childNode):
                        self.pathCost=childNode.cost
                        self.pathExist=True
                        return 1
                    frontier.enqueue(childNode)

    def dls_recursive(self,node,limit):
        if self.goal_test(node):
            self.pathCost=node.cost
            return 1
        elif limit==0:
            return self.cutOffValue
        else:
            self.cutOffOccurred=False
            for action in get_actions(self.mazeMap,node.state):
                childState = None
                if action == "right":
                    childState = (node.state[0], node.state[1] + 2)
                elif action == "left":
                    childState = (node.state[0], node.state[1] - 2)
                elif action == "up":
                    childState = (node.state[0] - 1, node.state[1])
                elif action == "down":
                    childState = (node.state[0] + 1, node.state[1])

                childNode = GraphNode(childState, node, action, node.cost + 1)
                self.nodeCount+=1
                result=self.dls_recursive(childNode,limit-1)
                if result==self.cutOffValue:
                    self.cutOffOccurred=True
                elif result!=0:
                    return result
            if self.cutOffOccurred:
                return self.cutOffValue
            return 0



    def dls_go(self,depth):
        '''
        This function perfroms DLS search
        :return:
        '''
        initialNode=GraphNode(self.startPoint,None,None,0)
        self.nodeCount=1
        return self.dls_recursive(initialNode,depth)


    def rds_go(self):
        for depth in range(self.maxDepth):
            result=self.dls_go(depth)
            if result != self.cutOffValue:
                self.pathExist=True
                self.finalDepth=depth
                return result

        # If no return happened in the the previous loop, it means goal was
        # not found.
        self.pathExist=False








a=Main()
a.init_map()
print("-----BFS-----")
a.bfs_go()
a.report("BFS")

print("\n-----RDS-----")
a.rds_go()
a.report("RDS")