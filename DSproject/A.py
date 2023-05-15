import random

import numpy as np
import time


def gs(i, j, startx, starty):
    return abs(i - startx) + abs(j - starty)


def h1(i, j, endx, endy):
    return 10 * (abs(i - endx) + abs(j - endy))


def h2(i, j, endx, endy):
    return pow(i - endx, 2) + pow(j - endy, 2)


def Astar(b, starty, startx, endy, endx):  # 下标从0起算
    startx += 1
    starty += 1
    endy=int(endy)
    endx=int(endx)
    endx += 1
    endy += 1
    a = 1 - b
    r = np.size(a, 0)
    c = np.size(a, 1)
    for i in range(0, r):
        for j in range(0, c):
            if a[i][j] != 0 and a[i][j] != 1:
                a[i][j] = 0
    if a[startx - 1, starty - 1] == 1:
        return []
    else:
        Close = [[startx, starty]]
        Opens = [[startx, starty]]
        crossings = []
        road = 100
        rows, cols = a.shape

        while True:
            if Close[-1] != [endx, endy]:
                Open = []
                i, j = Close[-1][0] - 1, Close[-1][1] - 1
                for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1), (i + 1, j + 1), (i + 1, j - 1),
                               (i - 1, j + 1), (i - 1, j - 1)]:
                    if [ni + 1, nj + 1] not in Opens and 0 <= ni < rows and 0 <= nj < cols and a[ni, nj] == 0:
                        Open.append([ni + 1, nj + 1])
                a[i, j] = road
                road = road + 1
                if Open:
                    Open = sorted(Open, key=lambda x: gs(x[0], x[1], startx, starty) + h2(x[0], x[1], endx, endy),
                                  reverse=True)
                    Opens.extend(Open)
                    Close.append(Open.pop())
                    if Open:
                        crossings.extend(Open)
                elif crossings:
                    next_way = crossings.pop()
                    road -= 1
                    Close.pop()
                    Close.append(next_way)
                else:
                    break
            else:
                print(endx-1,endy-1,'ok')
                a[endx - 1, endy - 1] = road
                break


        directionlist = [[0, 1], [0, -1], [1, 0], [-1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]
        l = len(Close)
        errorindex = []
        # print(Close)
        for i in range(1, l):
            if (np.array(Close[i]) - np.array(Close[i - 1])).tolist() not in directionlist:
                for j in range(i - 1, 1, -1):
                    if (np.array(Close[i]) - np.array(Close[j])).tolist() not in directionlist:
                        errorindex.append(j)
                    else:
                        break
            else:
                i += 1
        ans = [[startx - 1, starty - 1]]
        for i in range(1, l):
            if i not in errorindex:
                x = (np.array(Close[i]) - 1).tolist()
                ans.append(x)
        if [0, 1] in ans and [1, 0] in ans:
            if ((np.array(ans[3]) - np.array([1, 0])).tolist()) in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                ans.remove([0, 1])
            else:
                ans.remove([1, 0])
        return ans


def getDirection(Close):
    size = len(Close)
    stepsize=100
    if size > stepsize:
        size = stepsize
    ans1 = np.array(Close[0:size - 1])
    ans2 = np.array(Close[1:size])
    ans = ans2 - ans1
    return ans.tolist()
