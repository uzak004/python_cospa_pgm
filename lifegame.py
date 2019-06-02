#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys


# ルールを適用して次世代を作成する関数
def rule(cells):
    # 隣接セルにアクセスするための方向を用意
    dir = ((-1, -1), ( 0, -1), ( 1, -1),
           (-1,  0),           ( 1,  0),
           (-1,  1), ( 0,  1), ( 1,  1))

    # 次世代の状態を保持する２次元リストを生成
    tcells = [[0] * 40 for i in range(40)]

    # 周辺部を除く全セルにルールを適用する２重ループ
    for y in range(1, 40 - 1):
        for x in range(1, 40 - 1):
            c = 0
            for d in dir:    # 生きている隣接セルの個数を数える
                if cells[y + d[1]][x + d[0]]  == 1:
                    c += 1
            if cells[y][x] == 0 and c == 3:    # ルール１を適用
                tcells[y][x] = 1
            if cells[y][x] == 1:
                if c == 2 or c == 3:    # ルール２を適用
                    tcells[y][x] = 1
                else:                   # ルール３を適用
                    tcells[y][x] = 0

    return tcells    # 次世代の２次元リストを返す

