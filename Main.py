from Library import *
from math import sqrt

class Main:
    def __init__(self):
        self.mazeMap=list()
        self.mazeMapPath=list()
        self.startPoint=None
        self.endPoint=None
        self.nodeCount=0
        self.pathCost=0
        self.pathExist=False
        self.pathActions=list()
        self.cutOffValue=90
        self.cutOffOccurred=False
        self.finalDepth=0
        self.maxDepth=20


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

    def create_path(self,node):
        self.mazeMapPath=self.mazeMap

        while (node.parent)!=None:
            self.pathActions.append(node.action)
            self.pathCost+=1
            MAPx=node.state[0]
            MAPy=node.state[1]
            rowString=self.mazeMapPath[MAPx]

            if (node.action in "right left") and  (not self.goal_test(node)):
                self.mazeMapPath[MAPx]=rowString[:MAPy]+"-"+rowString[MAPy+1:]
            elif (node.action in "up down") and (not self.goal_test(node)):
                    self.mazeMapPath[MAPx]=rowString[:MAPy]+"|"+rowString[MAPy+1:]
            node=node.parent
        # reverse the order
        self.pathActions.reverse()

        # print maze map for the algorithms
        for row in self.mazeMapPath:
            print(row)

    def clear_counters(self):
        self.pathActions = []
        self.pathCost = 0
        self.nodeCount = 0

    def report(self,algorithm):
        if self.pathExist is False:
            print("No path to goal :(")
            print("#Node created: ",self.nodeCount)
        else:
            print("#Node created: ",self.nodeCount)
            print("Path cost is: ",self.pathCost)
            if algorithm=="RDS":
                print("Depth: ",self.finalDepth)

            print("Path Actions: "," ".join(self.pathActions))




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
                        self.pathExist=True
                        self.create_path(childNode)
                        return 1
                    frontier.enqueue(childNode)

    def dls_recursive(self,node,limit):
        if self.goal_test(node):
            self.create_path(node)
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
                print("res", result)
                return result

        # If no return happened in the the previous loop, it means goal was
        # not found.
        self.pathExist=False


    def heuristic(self,nodeState):
        # EP: end point
        EPx=self.endPoint[0]
        EPy=self.endPoint[1]
        x=nodeState[0]
        y=nodeState[1]
        
        return round(sqrt((abs(x-EPx))**2 + (abs(y-EPy))**2))

    def a_star(self):
        rootNode=GraphNode(self.startPoint,None,None,self.heuristic(self.startPoint))
        frontier=Queue()
        frontier.enqueue(rootNode)
        explored=list()
        while(1):
            if frontier.isempty():
                return 0
            node=frontier.dequeue()
            if self.goal_test(node):
                self.pathExist=True
                self.create_path(node)

                return 1
            explored.append(node.state)
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
                self.nodeCount += 1

                if (frontier.state_exist(childNode.state)) or (childNode.state not in explored):
                    frontier.enqueue(childNode)
                    frontier.queue.sort(key=lambda x: x.cost)

                else:
                    states= [node.state for node in frontier.get_queue()]
                    if (childState in states):
                        index=states.index(childState)
                        
                        if (self.heuristic(childState) + childNode.cost ) < frontier.get_queue().index(index).cost + self.heuristic(frontier.get_queue().index(index)):
                            frontier.queue[index]=childNode



obj=Main()



obj.init_map()
print("-------------")
print("     BFS     ")
print("-------------")

obj.bfs_go()
obj.report("BFS")
obj.clear_counters()
print("\n\n")

print("-------------")
print("     RDS     ")
print("-------------")
obj.rds_go()
obj.report("RDS")
obj.clear_counters()
print("\n\n")


print("-------------")
print("     A*     ")
print("-------------")
obj.a_star()
obj.report("A*")


