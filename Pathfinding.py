from queue import PriorityQueue
import numpy
from PIL import Image, ImageDraw

class State(object):
    def __init__(self, value, location, parent, start=0, goal=0):
        self.children = []
        self.parent = parent
        self.location = location
        self.value = value
        self.dist = 0
        if parent:
            self.path = parent.path[:]
            self.path.append(location)
            self.start = parent.start
            self.goal = parent.goal
        else:
            self.path = [location]
            self.start = start
            self.goal = goal

    def getDist(self):
        pass

    def createChildren(self):
        pass

class Sub_State(State):
    def __init__(self, value, location, parent, start=0, goal=0):
        super(Sub_State, self).__init__(value, location, parent, start, goal)
        self.dist = self.getDist()

    def getDist(self):
        if self.parent:
            return self.goal - self.location[1] + abs(self.value - self.parent.value)
        return 100000

    def createChildren(self):
        if self.location[0] > 0:
            self.children.append(Sub_State(getValue(self.location[0] - 1, self.location[1]), (self.location[0] - 1, self.location[1]), self, self.start, self.goal))
            try: self.children.append(Sub_State(getValue(self.location[0] - 1, self.location[1] + 1), (self.location[0] - 1, self.location[1] + 1), self, self.start, self.goal))
            except: pass
        if self.location[1] > 0:
            self.children.append(Sub_State(getValue(self.location[0], self.location[1] - 1), (self.location[0], self.location[1] - 1), self, self.start, self.goal))
            try: self.children.append(Sub_State(getValue(self.location[0] + 1, self.location[1] - 1), (self.location[0] + 1, self.location[1] - 1), self, self.start, self.goal))
            except: pass
        if self.location[0] > 0 and self.location[1] > 0:
            self.children.append(Sub_State(getValue(self.location[0] - 1, self.location[1] - 1), (self.location[0] - 1, self.location[1] - 1), self, self.start, self.goal))
        try:
            self.children.append(Sub_State(getValue(self.location[0] + 1, self.location[1]), (self.location[0] + 1, self.location[1]), self, self.start, self.goal))
            self.children.append(Sub_State(getValue(self.location[0], self.location[1] + 1), (self.location[0], self.location[1] + 1), self, self.start, self.goal))
            self.children.append(Sub_State(getValue(self.location[0] + 1, self.location[1] + 1), (self.location[0] + 1, self.location[1] + 1), self, self.start, self.goal))
        except: pass

    def __lt__(self, other):
        return self.getDist() < other.getDist()


class AStar_Solver:
    def __init__(self, start, goal):
        self.path = []
        self.visited = []
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal

    def solve(self):
        startState = Sub_State(getValue(self.start[0], self.start[1]), (self.start[0], self.start[1]), 0, self.start, self.goal)
        startState.createChildren()
        self.priorityQueue.put(startState)
        while not self.path and self.priorityQueue.qsize():
            closestChild = self.priorityQueue.get()
            closestChild.createChildren()
            for child in closestChild.children:
                if child.location not in self.visited:
                    self.visited.append(child.location)
                    if not child.dist:
                        self.path = child.path
                        break
                    self.priorityQueue.put(child)
        if not self.path: print('Goal is impossible')
        return self.path

def getValue(r, c): return MAP[r][c]


FILE = "Colorado_844x480.dat"
MAP = numpy.loadtxt(FILE)
im = Image.open("plainMountains.png")
draw = ImageDraw.Draw(im)

if __name__ == '__main__':
    min_path = None
    goal = len(MAP[0]) - 1
    print('starting...')
    for x in range(len(MAP)):
        start = [x, 0]
        solver = AStar_Solver(start, goal)
        path = solver.solve()
        if not min_path or len(min_path) > len(path): min_path = path
        print(start)
    print(min_path)
    draw = ImageDraw.Draw(im)
    for point in min_path:
        draw.point((point[1], point[0]), 'red')
    im.show()

