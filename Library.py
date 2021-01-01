class GraphNode:
    def __init__(self,state,parent,action,cost):
        self.state=state
        self.parent=parent
        self.action=action
        self.cost=cost


class Queue:
    def __init__(self):
        self.queue=list()
    def enqueue(self,node):
        self.queue.append(node)
    def dequeue(self):
        node=self.queue[0]
        self.queue.__delitem__(0)
        return node

    def isempty(self):
        if len(self.queue)==0:
            return 1
        return 0

    def state_exist(self, state):
        if state in self.queue:
            return 1
        return 0

def get_actions(mazeMap,state):
    '''
    This function receive maze map and current nodes state , and then returns
    all possible actions that can taken from that state
    :param mazeMap: 20x20 map
    :param state: State of the current node
    :return: All possible actions
    '''

    possibleActions=list()
    x=state[0]
    y=state[1]
    if x==0 and y==0:
        if mazeMap[0][2]!="*":
            possibleActions.append("right")
        if mazeMap[1][0]!="*":
            possibleActions.append("down")
    elif x==0 and y==19:
        if mazeMap[0][17]!="*":
            possibleActions.append("left")
        if mazeMap[1][19]!="*":
            possibleActions.append("down")

    elif x==19 and y==0:
        if mazeMap[18][0]!="*":
            possibleActions.append("up")
        if mazeMap[19][2]!="*":
            possibleActions.append("right")
    elif x==19 and y==19:
        if mazeMap[19][17]!="*":
            possibleActions.append("left")
        if mazeMap[18][19]!="*":
            possibleActions.append("up")
    elif x==0:
        if mazeMap[0][y+2] != "*":
            possibleActions.append("right")
        if mazeMap[0][y-2] != "*":
            possibleActions.append("left")
        if mazeMap[1][y] != "*":
            possibleActions.append("down")

    elif x==19:
        if mazeMap[0][y+2] != "*":
            possibleActions.append("right")
        if mazeMap[0][y-2] != "*":
            possibleActions.append("left")
        if mazeMap[18][y] != "*":
            possibleActions.append("up")

    elif y==0:
        if mazeMap[x-1][0] != "*":
            possibleActions.append("up")
        if mazeMap[x+1][0] != "*":
            possibleActions.append("down")
        if mazeMap[x][y+2] != "*":
            possibleActions.append("right")

    elif y==19:
        if mazeMap[x-1][0] != "*":
            possibleActions.append("up")
        if mazeMap[x+1][0] != "*":
            possibleActions.append("down")
        if mazeMap[x][y-2] != "*":
            possibleActions.append("left")

    else:
        if mazeMap[x-1][y] != "*":
            possibleActions.append("up")
        if mazeMap[x+1][y] != "*":
            possibleActions.append("down")
        if mazeMap[x][y-2] != "*":
            possibleActions.append("left")
        if mazeMap[x][y+2] != "*":
            possibleActions.append("right")


    return possibleActions