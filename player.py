from random import randint


class Player:
    def __init__(self, start_y, start_x, map, color):
        self.functionDict = {0: self.goDownRight, 1: self.goRight, 2: self.goUpRight, 3: self.goUpLeft, 4: self.goLeft,
                             5: self.goDownLeft}
        self.start_x = start_x
        self.start_y = start_y
        self.prev_start_x = start_x
        self.prev_start_y = start_y
        self.x = 0
        self.y = 0
        self.alive = True
        self.moved = False
        self.map = map
        self.prev_rand = 0
        self.riflePositions = [0, 5, 4, 3, 2, 1]
        self.rifle = self.riflePositions[0]
        self.color = color
        if self.color != 2:
            self.map.updateMap(self)

    def updatePrev(self):
        self.prev_start_x = self.start_x
        self.prev_start_y = self.start_y

    def walk(self):
        if self.map.isWalkable(self.y, self.x):
            self.updatePrev()
            self.start_y = self.y
            self.start_x = self.x
        self.map.updateMap(self)

    def goLeft(self):
        self.x = self.start_x - 1
        self.y = self.start_y

    def goRight(self):
        self.x = self.start_x + 1
        self.y = self.start_y

    def goUpRight(self):
        self.x = self.start_x
        self.y = self.start_y - 1
        if self.start_y % 2:
            self.x += 1

    def goDownRight(self):
        self.x = self.start_x
        self.y = self.start_y + 1
        if self.start_y % 2:
            self.x += 1

    def goUpLeft(self):
        self.x = self.start_x
        self.y = self.start_y - 1
        if not self.start_y % 2:
            self.x -= 1

    def goDownLeft(self):
        self.x = self.start_x
        self.y = self.start_y + 1
        if not self.start_y % 2:
            self.x -= 1

    def rifleLeftRotate(self):
        self.riflePositions.insert(0, self.riflePositions.pop())

    def rifleRightRotate(self):
        self.riflePositions.append(self.riflePositions.pop(0))

    def goRandom(self):
        r = randint(0, 1)
        if r:
            self.functionDict[self.prev_rand]()
            self.walk()
        else:
            r = randint(0, 5)
            self.prev_rand = r
            self.functionDict[self.prev_rand]()
            self.walk()

    def moveBullet(self):
        self.functionDict[self.rifle]()
        self.updatePrev()
        self.start_y = self.y
        self.start_x = self.x
