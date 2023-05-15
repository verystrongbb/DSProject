import random
from Maze import PrimMaze
from settings import *
import pygame
import numpy as np
from block import Block
from trap import Trap


# -----------------------------------对象定义---------------------------------
class myMap:
    def __init__(self, screen, all_sprites):
        super().__init__()
        # modify maz
        m = PrimMaze()
        self.Matrix = m.displaymaze()
        self.mazeMatrix = m.addtrap(0.6)
        self.door1, self.door2, self.door3, self.key1, self.key2, self.key3 = m.adddoors(self.mazeMatrix)
        # self.mazeMatrix = [[1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        #              [1, 0, 1, 8, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 8, 0, 1],
        #              [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1],
        #              [1, 8, 1, 0, 1, 1, 0, 1, 1, 1, 0, 8, 0, 1, 1, 1, 0, 1, 0, 1],
        #              [0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1],
        #              [1, 1, 0, 1, 1, 8, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
        #              [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        #              [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 8, 1],
        #              [1, 0, 0, 8, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 8, 0, 0, 0, 1, 1],
        #              [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        #              [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
        #              [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 0, 1, 0, 0, 1],
        #              [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
        #              [1, 1, 8, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        #              [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1],
        #              [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 8, 1, 8, 1, 1, 1, 1, 1, 1],
        #              [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #              [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8],
        #              [0, 0, 1, 8, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
        #              [1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1]]
        self.mazerow = np.shape(self.mazeMatrix)[0]
        self.mazecol = np.shape(self.mazeMatrix)[1]

        self.MoveArea = [[1 for _ in range(0, GAME_SCREEN_WIDTH)] for _ in range(0, GAME_SCREEN_HEIGHT)]

        self.Room_unit_Row = 5
        self.Room_unit_Col = 5

        self.RoomRow = self.mazerow // self.Room_unit_Row + 2
        self.RoomCol = self.mazecol // self.Room_unit_Col + 2
        # define para
        self.screen = screen

        self.xl = GAME_SCREEN_WIDTH // self.mazecol
        self.yl = GAME_SCREEN_HEIGHT // self.mazerow

        self.roomxl = GAME_SCREEN_WIDTH // self.RoomCol
        self.roomyl = GAME_SCREEN_HEIGHT // self.RoomRow

        self.cell_row = range(0, GAME_SCREEN_HEIGHT, self.yl)
        self.cell_col = range(0, GAME_SCREEN_WIDTH, self.xl)

        self.all_sprites = all_sprites
        self.block = Block(self.all_sprites)
        self.trap = Trap(self.all_sprites)

    # def drawWall(self):
    #     self.block.create_block_tile( self.mazeMatrix)
    #     self.block.block_sprites.draw(self.screen)
    #     for i in range(0, self.mazerow):
    #         for j in range(0, self.mazecol):
    #             if self.mazeMatrix[i][j] == 0:
    #                 for k in range(i * self.yl, (i + 1) * self.yl):
    #                     for p in range(j * self.xl, (j + 1) * self.xl):
    #                         self.MoveArea[k][p] = 0
    def drawRoom(self, x, y):
        room = self.toRoom(self.mazeMatrix, y, x)
        self.pr = room
        self.block.create_block_tile(room, self.roomyl, self.roomxl)
        self.block.block_sprites.draw(self.screen)
        self.trap.create_trap_tile(room, self.roomyl, self.roomxl)
        self.trap.trap_sprites.draw(self.screen)
        for i in range(0, self.RoomRow):
            for j in range(0, self.RoomCol):
                if room[i][j] == 0:
                    for k in range(max(i * self.roomyl - 32, 0),
                                   min((i + 1) * self.roomyl + 32, GAME_SCREEN_HEIGHT - 1)):
                        for p in range(max(j * self.roomxl - 32, 0), min((j + 1) * self.roomxl + 32,
                                                                         GAME_SCREEN_WIDTH - 1)):
                            self.MoveArea[k][p] = 0


    def getRoomBirthPos(self, RoomNO):
        room = self.toRoom(self.mazeMatrix, RoomNO[1],RoomNO[0])
        movepath = self.MoveArea
        for i in range(0, self.RoomRow):
            for j in range(0, self.RoomCol):
                if room[i][j] == 0:
                    for k in range(max(i * self.roomyl - 32, 0),
                                   min((i + 1) * self.roomyl + 32, GAME_SCREEN_HEIGHT - 1)):
                        for p in range(max(j * self.roomxl - 32, 0), min((j + 1) * self.roomxl + 32,
                                                                         GAME_SCREEN_WIDTH - 1)):
                             movepath[k][p] = 0


        birthPos = []
        err = 30
        for i in range(err, GAME_SCREEN_HEIGHT - err):
            for j in range(err, GAME_SCREEN_WIDTH - err):
                if movepath[i][j] == 1 and (movepath[i + k][j + p] == 1 for k, p in [-err, err]):
                    birthPos.append((j, i))

        # print(Player_birth)
        i = random.randint(0, len(birthPos) - 1)
        Enemy_birth = birthPos[i]
        return Enemy_birth

    def toRoom(self, maze, i, j):
        room = np.zeros((self.RoomRow, self.RoomCol))
        for k in range(1, self.RoomRow - 1):
            for p in range(1, self.RoomCol - 1):
                room[k][p] = maze[k - 1 + i * (self.RoomRow - 2)][p - 1 + j * (self.RoomCol - 2)]
        for r in range(1, self.RoomRow - 1):
            if j < self.Room_unit_Col - 1:
                if maze[r - 1 + i * (self.RoomRow - 2)][(j + 1) * (self.RoomCol - 2) - 1] != 0 and \
                        maze[r - 1 + i * (self.RoomRow - 2)][(j + 1) * (self.RoomCol - 2)] != 0:
                    room[r][self.RoomCol - 1] = 1
            if j > 0:
                if maze[r - 1 + i * (self.RoomRow - 2)][j * (self.RoomCol - 2) - 1] != 0 and \
                        maze[r - 1 + i * (self.RoomRow - 2)][j * (self.RoomCol - 2)] != 0:
                    room[r][0] = 1

        for c in range(1, self.RoomCol - 1):
            if i < self.Room_unit_Row - 1:
                if maze[(i + 1) * (self.RoomRow - 2) - 1][c - 1 + j * (self.RoomCol - 2)] != 0 and \
                        maze[(i + 1) * (self.RoomRow - 2)][c - 1 + j * (self.RoomCol - 2)] != 0:
                    room[self.RoomRow - 1][c] = 1
            if i > 0:
                if maze[i * (self.RoomRow - 2) - 1][c - 1 + j * (self.RoomCol - 2)] != 0 and \
                        maze[i * (self.RoomRow - 2)][c - 1 + j * (self.RoomCol - 2)] != 0:
                    room[0][c] = 1

        return room

    def initMoveArea(self):

        self.MoveArea = [[1 for _ in range(0, GAME_SCREEN_WIDTH)] for _ in range(0, GAME_SCREEN_HEIGHT)]

    def printRoom(self):
        print(self.pr)

    def getRoomRC(self):

        return [self.Room_unit_Row, self.Room_unit_Col]

    def getBlock(self):

        return self.block.getBlockGroup()

    def getTrap(self):

        return self.trap.getTrapGroup()

    def getMoveArea(self):

        return self.MoveArea

    def getMovePos(self):
        movepos = []
        for i in range(0, GAME_SCREEN_HEIGHT):
            for j in range(0, GAME_SCREEN_WIDTH):
                if self.MoveArea[i][j] == 1:
                    movepos.append((i, j))
        return movepos

    def getmaze(self):
        return self.mazeMatrix

    def getmazerow(self):
        return self.mazerow

    def getmazecol(self):
        return self.mazecol

    def getcell_col(self):
        return self.cell_col

    def getcell_row(self):
        return self.cell_row

    def MazeGenerator(self):
        return self.mazeMatrix

    def has_path(self, maze):
        width = len(maze[0])
        height = len(maze)
        queue = [(0, 0)]
        visited = set()
        while queue:
            x, y = queue.pop(0)
            if (x, y) == (width - 1, height - 1):
                return True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = x + dx, y + dy
                if new_x >= width or new_x < 0 or new_y >= height or new_y < 0:
                    continue
                if maze[new_y][new_x] == 1 and (new_x, new_y) not in visited:
                    queue.append((new_x, new_y))
                    visited.add((new_x, new_y))
        return False