#!/usr/bin/python3.8
from Library import *
from math import sqrt
from sys import argv
from random import choice

from argparse import ArgumentParser


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
        self.maxDepth=15
        self.supportedAlgorithms=["bfs","a*","rds"]


    def init_map(self,file):
        if file is not None:
            fh=open(file)
            # row[:-1] for eliminating line feed
            self.mazeMap=[row[:-1] for row in  fh.readlines()]
            fh.close()
            for i in range(20):
                if "S" in self.mazeMap[i]:
                    self.startPoint=(i,(self.mazeMap[i].index("S")))
                if "G" in self.mazeMap[i]:
                    self.endPoint=(i,(self.mazeMap[i].index("G")))

        else:
            tmpList=list()
            for i in range(20):
                for j in range(20):
                    tmpList.append(choice(" *"))
                    
                self.mazeMap.append(" ".join(tmpList))
                tmpList=[]

            # choosing random x,y for source
            sourceX=choice([i for i in range(20)])
            sourceY=choice([i for i in range(40) if i%2==0])
            self.startPoint=(sourceX,sourceY)
           
            # choosing random x,y for goal
            goalX=choice([i for i in range(20) if i!=sourceX])
            goalY=choice([i for i in range(40) if i%2==0 and i!=sourceY])
            self.endPoint=(goalX,goalY)

            self.mazeMap[sourceX]=self.mazeMap[sourceX][:sourceY]+"S"+self.mazeMap[sourceX][sourceY+1:]

            self.mazeMap[goalX]=self.mazeMap[goalX][:goalY]+"G"+self.mazeMap[goalX][goalY+1:]

            print("----------------------------------------")
            print("----------------------------------------")
            print("              RANDOM MAP                ")
            print("----------------------------------------")
            print("----------------------------------------\n")
            
            
            # print new map

            for row in self.mazeMap:
                print(row)
                
            print()

          


    def run_algorithms(self,algorithms):
        if algorithms is None:
            algorithms=self.supportedAlgorithms

        for algorithm in algorithms:
            if algorithm in self.supportedAlgorithms:
                if algorithm=="bfs":
                    print("-------------")
                    print("     BFS     ")
                    print("-------------")

                    self.bfs_go()
                    self.report("BFS")

                elif algorithm=="rds":
                    
                    print("-------------")
                    print("     RDS     ")
                    print("-------------")
                    self.rds_go()
                    self.report("RDS")

                elif algorithm=="a*":

                    print("-------------")
                    print("     A*     ")
                    print("-------------")
                    self.a_star()
                    self.report("A*")
  
                self.clear_counters()
                print("\n\n")
            else:
                print("%% Algorithm '{0}' is unknown\n".format(algorithm))




           
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







program=Main()
parser = ArgumentParser()
parser.add_argument("-f","--file")
parser.add_argument("-a","--algorithms",nargs='+')
args = parser.parse_args()


program.init_map(args.file)

program.run_algorithms(args.algorithms)



