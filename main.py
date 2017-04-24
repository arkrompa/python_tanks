import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtGui import QPainter, QPainterPath
from map import *
from player import *
from PyQt5.QtCore import QTimer


class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton('New game', self)
        self.button_enemy = QPushButton('Add enemy', self)
        self.init_buttons()
        self.bit_map = QtGui.QPixmap(SCREEN_WIDTH - BUTTONS_MARGIN + 3*HEX_SIZE, SCREEN_HEIGHT)
        self.timer = QTimer()
        self.bullet_timer = QTimer()
        self.key_timer = QTimer()
        self.key_timer_done = True
        self.map = hexMap()
        self.map.createHexagons()
        self.map.fillEdges()
        self.map.constantMapInit()
        self.humans = []
        self.enemies = []
        self.bullets = []
        self.initPlayers()
        self.drawMap()
        self.initUI()
        self.qp = QPainter()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(200)
        self.bullet_timer.timeout.connect(self.bullet_update)
        self.bullet_timer.start(100)
        self.key_timer.timeout.connect(self.timer_done)

    def init_buttons(self):
        self.button.clicked.connect(self.handleButton)
        self.button.setGeometry(SCREEN_WIDTH - BUTTONS_MARGIN + 5*HEX_SIZE, 50, BUTTONS_MARGIN * 0.5, 50)
        self.button_enemy.clicked.connect(self.handleButton_enemy)
        self.button_enemy.setGeometry(SCREEN_WIDTH - BUTTONS_MARGIN + 5*HEX_SIZE, 120, BUTTONS_MARGIN * 0.5, 50)

    def handleButton(self):
        self.newGame()

    def handleButton_enemy(self):
        while True:
            x = randint(0, 19)
            y = randint(0, 19)
            if self.map.map_matrix[y][x].color_key == 0:
                break

        self.enemies.append(Player(y, x, self.map, 7))

    def newGame(self):
        self.enemies.clear()
        self.humans.clear()
        self.bullets.clear()

        self.timer = QTimer()
        self.bullet_timer = QTimer()
        self.key_timer = QTimer()
        self.key_timer_done = True
        self.map = hexMap()
        self.map.createHexagons()
        self.map.fillEdges()
        self.map.constantMapInit()
        self.humans = []
        self.enemies = []
        self.bullets = []
        self.initPlayers()
        self.drawMap()
        self.initUI()
        self.qp = QPainter()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(200)
        self.bullet_timer.timeout.connect(self.bullet_update)
        self.bullet_timer.start(100)
        self.key_timer.timeout.connect(self.timer_done)

    def bullet_update(self):

        for bullet in self.bullets:
            if self.map.deleteFire(bullet):
                self.bullets.remove(bullet)
                self.drawSingleHex(bullet.start_y, bullet.start_x)
            else:
                bullet.moveBullet()
                self.drawSingleHexColor(bullet.prev_start_y, bullet.prev_start_x, LIGHT_GRAY)
                self.drawSingleCircle(bullet.start_y, bullet.start_x)
            for human in self.humans:
                if bullet.start_y == human.start_y and bullet.start_x == human.start_x:
                    self.humans.remove(human)

            for enemy in self.enemies:
                if bullet.start_y == enemy.start_y and bullet.start_x == enemy.start_x:
                    self.enemies.remove(enemy)
        self.repaint()

    def update_game(self):
        for enemy in self.enemies:
            enemy.goRandom()
            self.drawSingleHex(enemy.prev_start_y, enemy.prev_start_x)
            self.drawSingleHex(enemy.start_y, enemy.start_x)
            self.drawRifle(self.map.map_matrix[enemy.start_y][enemy.start_x], enemy.riflePositions[0])

            r = randint(0, 1)
            if r:
                enemy.rifleLeftRotate()
            else:
                enemy.rifleRightRotate()

            r = randint(0, 4)
            if r == 0:
                x = Player(enemy.start_y, enemy.start_x, self.map, 2)
                x.rifle = enemy.riflePositions[0]
                x.moveBullet()
                self.drawSingleCircle(x.start_y, x.start_x)
                self.bullets.append(x)

        for human in self.humans:
            self.drawSingleHex(human.start_y, human.start_x)
            self.drawRifle(self.map.map_matrix[human.start_y][human.start_x], human.riflePositions[0])
        self.repaint()

    def initPlayers(self):
        self.humans.append(Player(5, 2, self.map, 3))
        self.enemies.append(Player(15, 15, self.map, 7))

    def initUI(self):
        self.setGeometry(20, 20, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setWindowTitle('Tanks')
        self.show()

    def paintEvent(self, e):
        self.qp.begin(self)
        self.qp.drawPixmap(0, 0, self.bit_map)
        self.qp.end()

    def drawMap(self):
        painter = QPainter()
        painter.setPen(GRAY)
        painter.begin(self.bit_map)
        painter.fillRect(0, 0, SCREEN_WIDTH - BUTTONS_MARGIN + 3*HEX_SIZE, SCREEN_HEIGHT, LIGHT_BLUE)
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                path = QPainterPath()
                path.addPolygon(self.map.map_matrix[i][j].hex_polygon)
                painter.fillPath(path, self.map.map_matrix[i][j].getColor())
                painter.drawPolygon(self.map.map_matrix[i][j].hex_polygon)
        painter.end()
        for human in self.humans:
            self.drawSingleHex(human.start_y, human.start_x)
            self.drawRifle(self.map.map_matrix[human.start_y][human.start_x], human.riflePositions[0])
        for enemy in self.enemies:
            self.drawSingleHex(enemy.start_y, enemy.start_x)
            self.drawRifle(self.map.map_matrix[enemy.start_y][enemy.start_x], enemy.riflePositions[0])
        self.repaint()

    def drawSingleHex(self, x, y):
        painter = QPainter()
        painter.setPen(GRAY)
        painter.begin(self.bit_map)
        path = QPainterPath()
        path.addPolygon(self.map.map_matrix[x][y].hex_polygon)
        painter.fillPath(path, self.map.map_matrix[x][y].getColor())
        painter.drawPolygon(self.map.map_matrix[x][y].hex_polygon)
        painter.end()

    def drawSingleHexColor(self, x, y, color):
        painter = QPainter()
        painter.setPen(GRAY)
        painter.begin(self.bit_map)
        path = QPainterPath()
        path.addPolygon(self.map.map_matrix[x][y].hex_polygon)
        painter.fillPath(path, color)
        painter.drawPolygon(self.map.map_matrix[x][y].hex_polygon)
        painter.end()

    def drawSingleCircle(self, x, y):
        painter = QPainter()
        painter.begin(self.bit_map)
        painter.setBrush(BROWN)
        painter.setPen(GRAY)
        painter.drawEllipse(self.map.map_matrix[x][y].center, 5, 5)
        painter.end()

    def drawRifle(self, hexagon, i):
        painter = QPainter()
        painter.setPen(GRAY)
        painter.begin(self.bit_map)
        path = QPainterPath()
        path.addPolygon(hexagon.getRiflePolygon(i))
        painter.fillPath(path, LIGHT_BLUE)
        painter.drawPolygon(hexagon.hex_polygon)
        painter.end()

    def timer_done(self):
        self.key_timer_done = True

    def keyPressEvent(self, e):
        key_pressed = e.key()
        if self.key_timer_done and self.humans:
            self.key_timer_done = False
            if key_pressed == QtCore.Qt.Key_4:
                self.humans[0].goLeft()
                self.humans[0].walk()

            elif key_pressed == QtCore.Qt.Key_6:
                self.humans[0].goRight()
                self.humans[0].walk()

            elif key_pressed == QtCore.Qt.Key_7:
                self.humans[0].goUpLeft()
                self.humans[0].walk()

            elif key_pressed == QtCore.Qt.Key_9:
                self.humans[0].goUpRight()
                self.humans[0].walk()

            elif key_pressed == QtCore.Qt.Key_1:
                self.humans[0].goDownLeft()
                self.humans[0].walk()

            elif key_pressed == QtCore.Qt.Key_3:
                self.humans[0].goDownRight()
                self.humans[0].walk()

            elif key_pressed == QtCore.Qt.Key_5:
                x = Player(self.humans[0].start_y, self.humans[0].start_x, self.map, 2)
                x.rifle = self.humans[0].riflePositions[0]
                x.moveBullet()
                self.drawSingleCircle(x.start_y, x.start_x)
                self.bullets.append(x)

            elif key_pressed == QtCore.Qt.Key_Q:
                self.humans[0].rifleLeftRotate()

            elif key_pressed == QtCore.Qt.Key_E:
                self.humans[0].rifleRightRotate()

            elif key_pressed == QtCore.Qt.Key_Escape:
                self.close()
            self.key_timer.start(200)

            self.drawSingleHex(self.humans[0].prev_start_y, self.humans[0].prev_start_x)
            self.drawSingleHex(self.humans[0].start_y, self.humans[0].start_x)
            self.drawRifle(self.map.map_matrix[self.humans[0].start_y][self.humans[0].start_x],
                           self.humans[0].riflePositions[0])
            self.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())
