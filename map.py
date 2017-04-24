from hexagon import *


class hexMap:
    def __init__(self):
        self.map_matrix = []

    def createHexagons(self):
        for y in range(MAP_SIZE):
            tmp_hex_list = []
            for x in range(MAP_SIZE):
                if y % 2:
                    tmp_hex_list.append(Hexagon(HEX_WIDTH_SPACING * (x + 3 / 2), HEX_HEIGHT_SPACING * (y + 1), 0))
                else:
                    tmp_hex_list.append(Hexagon(HEX_WIDTH_SPACING * (x + 1), HEX_HEIGHT_SPACING * (y + 1), 0))

            self.map_matrix.append(tmp_hex_list)

    def fillEdges(self):
        for i in range(MAP_SIZE):
            self.map_matrix[0][i].color_key = 10
            self.map_matrix[MAP_SIZE - 1][i].color_key = 10
            self.map_matrix[i][0].color_key = 10
            self.map_matrix[i][MAP_SIZE - 1].color_key = 10
        self.map_matrix[0][MAP_SIZE - 1].color_key = 10

    def constantMapInit(self):
        self.map_matrix[9][9].color_key = 9
        self.map_matrix[10][10].color_key = 9
        self.map_matrix[11][11].color_key = 9
        self.map_matrix[12][11].color_key = 9
        self.map_matrix[11][12].color_key = 9
        self.map_matrix[11][13].color_key = 9
        self.map_matrix[11][10].color_key = 9
        self.map_matrix[12][10].color_key = 9
        self.map_matrix[13][10].color_key = 9
        self.map_matrix[14][10].color_key = 9
        self.map_matrix[15][10].color_key = 9
        self.map_matrix[16][10].color_key = 9
        self.map_matrix[17][10].color_key = 9

        self.map_matrix[5][8].color_key = 8
        self.map_matrix[4][8].color_key = 8
        self.map_matrix[4][9].color_key = 8
        self.map_matrix[3][8].color_key = 8
        self.map_matrix[3][9].color_key = 8
        self.map_matrix[5][9].color_key = 8

        self.map_matrix[5 + 10][8 - 6].color_key = 8
        self.map_matrix[4 + 10][8 - 6].color_key = 8
        self.map_matrix[4 + 10][9 - 6].color_key = 8
        self.map_matrix[3 + 10][8 - 6].color_key = 8
        self.map_matrix[3 + 10][9 - 6].color_key = 8
        self.map_matrix[5 + 10][9 - 6].color_key = 8

        self.map_matrix[4][14].color_key = 9
        self.map_matrix[4][15].color_key = 9
        self.map_matrix[4][16].color_key = 9
        self.map_matrix[6][15].color_key = 9
        self.map_matrix[7][15].color_key = 9
        self.map_matrix[8][15].color_key = 9
        self.map_matrix[9][15].color_key = 9
        self.map_matrix[4][13].color_key = 9

        self.map_matrix[2][2].color_key = 9
        self.map_matrix[2][3].color_key = 9
        self.map_matrix[3][3].color_key = 9
        self.map_matrix[4][4].color_key = 9
        self.map_matrix[4][5].color_key = 9
        self.map_matrix[5][5].color_key = 9

    def isWalkable(self, y, x):
        if 0 < y < MAP_SIZE and 0 < x < MAP_SIZE:
            if self.map_matrix[y][x].color_key < 3:
                return True
            else:
                return False
        else:
            return False

    def deleteFire(self, fire):

        if self.map_matrix[fire.start_y][fire.start_x].color_key > 8:
            return True

        elif self.map_matrix[fire.start_y][fire.start_x].color_key > 0:
            self.map_matrix[fire.start_y][fire.start_x].color_key = 0
            return True

        elif self.map_matrix[fire.start_y][fire.start_x].color_key == 0:
            return False

    def updateMap(self, agent):
        self.map_matrix[agent.prev_start_y][agent.prev_start_x].color_key = 0
        self.map_matrix[agent.start_y][agent.start_x].color_key = agent.color

