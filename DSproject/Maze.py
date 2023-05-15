import numpy as np
import random
import A


class PrimMaze:
    def __init__(self):
        self.image = np.array([])  # 类型备份，因为后面我需要迷宫成2值状态
        self.size = (20, 20)
        self.maze = self.initmaze()  # 初始化
        self.size = np.shape(self.maze)
        self.seeker = self.initseeker()
        self._walls = []  # 墙列表
        self.createmaze()  # 生成迷宫

    # 初始化规格
    def initmaze(self):
        x, y = self.size
        maze = np.zeros(self.size)
        for i in range(x):
            for j in range(y):
                if i % 2 == 1 or j % 2 == 1:
                    maze[i, j] = 1
        return maze

    # 初始化seeker
    def initseeker(self):
        self.maze[0, 0] = 2
        return 0, 0

    # 将墙插入列表
    def insertwall(self):
        size = np.shape(self.maze)

        if self.seeker[0] + 1 < size[0] and self.maze[self.seeker[0] + 1, self.seeker[1]] == 1:
            self._walls.append((self.seeker[0] + 1, self.seeker[1]))
        if self.seeker[0] - 1 > 0 and self.maze[self.seeker[0] - 1, self.seeker[1]] == 1:
            self._walls.append((self.seeker[0] - 1, self.seeker[1]))
        if self.seeker[1] + 1 < size[1] and self.maze[self.seeker[0], self.seeker[1] + 1] == 1:
            self._walls.append((self.seeker[0], self.seeker[1] + 1))
        if self.seeker[1] - 1 > 0 and self.maze[self.seeker[0], self.seeker[1] - 1] == 1:
            self._walls.append((self.seeker[0], self.seeker[1] - 1))
        self._walls = list(set(self._walls))

    # 摧毁墙
    def destroywall(self, wall):
        x = wall[0]
        y = wall[1]

        # 纵墙
        if wall[0] % 2 == 1:
            # 上边和下边都访问过，无效墙
            if x <= 18:
                if self.maze[x - 1, y] == 2 and self.maze[x + 1, y] == 2:
                    self.maze[x, y] = 3
                    return True
                # 穿透
                else:
                    self.maze[x, y] = 2
                    if self.maze[x - 1, y] == 2:
                        self.maze[x + 1, y] = 2
                        self.seeker = (x + 1, y)
                        return True
                    elif self.maze[x + 1, y] == 2:
                        self.maze[x - 1, y] = 2
                        self.seeker = (x - 1, y)
                        return True
            else:
                if self.maze[x - 1, y] == 2:
                    self.maze[x, y] = 3
                    return True
                # 穿透
                else:
                    self.maze[x, y] = 2
                    if self.maze[x - 1, y] == 2:
                        self.maze[x + 1, y] = 2
                        self.seeker = (x + 1, y)
                        return True
        # 横墙
        if wall[1] % 2 == 1:
            # 左边和右边都访问过，无效墙
            if y <= 18:
                if self.maze[x, y - 1] == 2 and self.maze[x, y + 1] == 2:
                    self.maze[x, y] = 3
                    return True
                # 穿透
                else:
                    self.maze[x, y] = 2
                    if self.maze[x, y - 1] == 2:
                        self.maze[x, y + 1] = 2
                        self.seeker = (x, y + 1)
                        return True
                    elif self.maze[x, y + 1] == 2:
                        self.maze[x, y - 1] = 2
                        self.seeker = (x, y - 1)
                        return True
        return False

    # 将迷宫初始化，
    def createmaze(self):
        while True:
            self.insertwall()
            temp = 0
            if np.shape(self._walls)[0] > 0:
                temp = self._walls.pop(random.randint(0, np.shape(self._walls)[0] - 1))
                self.destroywall(temp)
            if not self._walls:
                break

    # 返回迷宫序列
    def displaymaze(self):  # 生成迷宫就创建个PrimMaze对象然后直接调用这玩意
        self.maze = 1 - (self.maze % 2)
        self.maze[0, 0] = 1
        self.maze[19, 19] = 1
        for i in range(1, 18):
            for j in range(1, 18):
                if self.maze[i][j] == 1 and (
                        self.maze[i - 1][j - 1] + self.maze[i - 1][j + 1] + self.maze[i + 1][j + 1] + self.maze[i + 1][
                    j - 1] == 1 and
                        self.maze[i][j - 1] + self.maze[i][j + 1] + self.maze[i - 1][j] + self.maze[i + 1][j] == 0):
                    for x, y in [(i + 1, j + 1), (i + 1, j - 1), (i - 1, j + 1), (i - 1, j - 1)]:
                        if self.maze[x][y] == 1:
                            r = random.randint(0, 1)
                            if r == 0:
                                self.maze[i][y] = 1
                            else:
                                self.maze[x][j] = 1
                            break

        # path = A.Astar(self.maze, 0, 0, 19, 19)
        # l = len(path)
        # for i in range(1, l):
        #
        #     if (np.array(path[i]) - np.array(path[i - 1])).tolist() in[[-1, -1], [-1, 1], [1, -1], [1, 1]]:
        rs = random.randint(0, 1)
        if rs == 0:
            self.maze[18][19] = 1
        else:
            self.maze[19][18] = 1
        return self.maze

    def addtrap(self, rate):  # 加陷阱
        for i in range(0, 19):
            for j in range(0, 19):
                if self.maze[i][j] == 1 and (
                        self.maze[i - 1, j] + self.maze[i + 1, j] + self.maze[i, j - 1] + self.maze[i, j + 1] >= 3
                        and self.maze[i - 1, j] + self.maze[i + 1, j] + self.maze[i, j - 1] + self.maze[
                            i, j + 1] < 8 and random.uniform(0, 1) < rate):
                    self.maze[i][j] = 8
        self.maze[0][0] = 1
        self.maze[19][19] = 1

        for row in self.maze:
            print(row)

        return self.maze

    def dfs(self, maze, path, x, y, step, door):
        if x != 19 and y != 19 and x != 0 and y != 0:
            if ((maze[x - 1][y - 1] + maze[x - 1][y] + maze[x - 1][y + 1] + maze[x][y - 1] + maze[x][y + 1] +
                 maze[x + 1][y - 1] + maze[x + 1][y] + maze[x + 1][y + 1]) % 8 == 1 and [x, y] not in path and maze[x][
                y] <= 2):
                return x, y, True
        elif x == 0 and y != 0:
            if ((maze[x][y - 1] + maze[x][y + 1] + maze[x + 1][y - 1] + maze[x + 1][y] + maze[x + 1][y + 1]) % 8 == 1
                    and [x, y] not in path and maze[x][y] <= 2):
                return x, y, True
        elif x != 0 and y == 0:
            if ((maze[x - 1][y] + maze[x - 1][y + 1] + maze[x][y + 1] + maze[x + 1][y] + maze[x + 1][y + 1]) % 8 == 1
                    and [x, y] not in path and maze[x][y] <= 2):
                return x, y, True

        if step == 0:
            return x, y, True

        if [x, y] in door:
            return -10086, -10086, False

        if x < 0 or y < 0:
            return -10086, -10086, False

        list1 = []
        if x != 19 and y != 19:
            for [xx, yy] in [[x - 1, y - 1], [x - 1, y], [x - 1, y + 1], [x, y - 1], [x, y + 1], [x + 1, y - 1],
                             [x + 1, y], [x + 1, y + 1]]:
                if xx != 19 and yy != 19:
                    if [xx, yy] not in path and maze[xx][yy] == 1 and [xx, yy] not in list1:
                        list1.append([xx, yy])
                        return self.dfs(maze, path, xx, yy, step - 1, door)

        return 0, 0, False

    def judge(self, maze, x, y):
        if ((maze[x - 1][y - 1] + maze[x - 1][y] + maze[x - 1][y + 1] + maze[x][y - 1] + maze[x][y + 1] +
             maze[x + 1][y - 1] + maze[x + 1][y] + maze[x + 1][y + 1]) % 8 == 2):
            return True
        elif ((maze[x - 1][y - 1] + maze[x - 1][y] + maze[x - 1][y + 1] + maze[x][y - 1] + maze[x][y + 1] +
               maze[x + 1][y - 1] + maze[x + 1][y] + maze[x + 1][y + 1]) % 8 == 3):
            if (maze[x - 1][y - 1] + maze[x - 1][y] + maze[x][y - 1]) % 8 == 3:
                return False
            elif (maze[x - 1][y + 1] + maze[x - 1][y] + maze[x][y + 1]) % 8 == 3:
                return False
            elif (maze[x + 1][y - 1] + maze[x + 1][y] + maze[x][y - 1]) % 8 == 3:
                return False
            elif (maze[x + 1][y + 1] + maze[x + 1][y] + maze[x][y + 1]) % 8 == 3:
                return False
            return True
        return False

    def adddoors(self, maze):  # 加门
        path = A.Astar(self.maze, 0, 0, 19, 19)
        size = len(path)
        predoor = []
        door = []
        key = [[], [], []]
        dd = [0]
        for i in range(0, size):
            x = path[i][0]
            y = path[i][1]
            if x != 19 and y != 19:
                if self.judge(maze, x, y):
                    predoor.append([x, y])
        l = len(predoor)
        # print(l)
        if [0, 0] in predoor:
            predoor.remove([0, 0])
        # print(predoor)
        d1 = int(l / 4 - 1)
        d2 = int(l / 2)
        d3 = int(l * 3 / 4 + 1)
        door.append(predoor[d1])
        door.append(predoor[d2])
        door.append(predoor[d3])
        dd.append(path.index(predoor[d1]))
        dd.append(path.index(predoor[d2]))
        dd.append(path.index(predoor[d3]))
        for i in range(1, 4):
            for j in range(dd[i - 1] + 1, dd[i] - 1):
                xx = path[j][0]
                yy = path[j][1]
                kx, ky, judge = self.dfs(self.maze, path, xx, yy, 100, door)
                if judge and maze[xx][yy] == 1:
                    key[i - 1].append([kx, ky])
            if len(key[i - 1]) == 0:
                key[i - 1].append(path[dd[i - 1 + 1]])

        if door[0] == key[0][-1]:
            door[0] = predoor[random.randint(d1 + 1, d2 - 1)]
        else:
            door[0] = predoor[random.randint(d1, d2 - 1)]

        if door[1] == key[1][-1]:
            door[1] = predoor[random.randint(d2 + 1, d3 - 1)]
        else:
            door[1] = predoor[random.randint(d2, d3 - 1)]

        if door[2] == key[2][-1]:
            door[2] = predoor[random.randint(d3 + 1, l - 2)]
        else:
            door[2] = predoor[random.randint(d3, l - 2)]

        return door[0], door[1], door[2], key[0][-1], key[1][-1], key[2][-1]

# # m = PrimMaze()
# # a = m.displaymaze()
# #
# # #a = 1 - (a % 2)
# #
# # for row in a:
# #     print(row)
# #
# # print('\n')
# #
# # p = A.Astar(a, 0, 0, 19, 19)
# #
# # print(p)
# #
# # b = m.addtrap(0.5)
# # for row in b:
# #     print(row)
# #
# # d1, d2, d3, k1, k2, k3 = m.adddoors(b)
# # print(d1, end=' ')
# # print(k1)
# # print(d2, end=' ')
# # print(k2)
# # print(d3, end=' ')
# # print(k3)
