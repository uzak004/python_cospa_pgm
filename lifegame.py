#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import MOUSEBUTTONDOWN, Rect, QUIT
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
                if cells[y + d[1]][x + d[0]] == 1:
                    c += 1
            if cells[y][x] == 0:
                if gen % 17 == 0:           # 世代数が17の倍数の時に増殖ルールを緩くする
                    if c >= 2:
                        tcells[y][x] = 1
                else:
                    if c == 3:    # ルール１を適用
                        tcells[y][x] = 1
            if cells[y][x] == 1:
                if c == 2 or c == 3:    # ルール２を適用
                    tcells[y][x] = 1
                else:                   # ルール３を適用
                    tcells[y][x] = 0

    return tcells    # 次世代の２次元リストを返す


pygame.init()
# サイズを設定して画面を生成
screen = pygame.display.set_mode((800, 800))
font = pygame.font.Font(None, 28)
# セルの状態を保持する2次元リストを生成
cells = [[0] * 40 for i in range(40)]
run = 0    # 実行フラグ
gen = 1    # 世代数


while True:    # シミュレーションを実行する無限ループ
    screen.fill((255, 255, 255))    # 背景を白にする

    if run == 1:
        gen += 1
        cells = rule(cells)
        pygame.time.wait(250)    # 250ミリ秒間プログラムを停止

    # セルを描画する2重ループ
    for y in range(0, 40):
        for x in range(0, 40):
            if cells[y][x] == 1:
                rect = Rect(x * 20, y * 20, 20, 20)    # ??? pygame.Rect じゃなくていいの？
                pygame.draw.rect(screen, (0, 255, 0), rect)

    # マウスからの入力を処理する
    for e in pygame.event.get():
        if e.type == MOUSEBUTTONDOWN and e.button == 1 and run == 0:
            mx, my = int(e.pos[0] / 20), int(e.pos[1] / 20)
            if mx == 0 or mx == 40 - 1 or my == 0 or my == 40 - 1:
                cells[my][mx] = 0    # 周縁部のセルは常に0にする
            else:
                # マウスクリックしたセルが0なら1に、1なら0にする
                cells[my][mx] = 1 - cells[my][mx]
        if e.type == MOUSEBUTTONDOWN and e.button == 2:
            run = 1 - run    # 実行フラグをフリップ
        if e.type == MOUSEBUTTONDOWN and e.button == 3 and run == 0:
            # シミュレーションをリセットする
            cells = [[0] * 40 for i in range(40)]
            gen = 1
        if e.type == QUIT:
            pygame.quit()
            sys.exit()

    s1 = "running" if run == 1 else "setting"
    s2 = "generation : " + str(gen)
    text = font.render(s1 + "   " + s2, True, (0, 0, 0))
    screen.blit(text, (1, 1))    # 画面に文字列を描く
    pygame.display.update()
