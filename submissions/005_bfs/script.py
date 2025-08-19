# bfs + 動的計画法みたいな方法で良い成績取ってる
import time
import heapq
import numpy as np

H, W = 50, 50


if __name__ == "__main__":
    # 入力の読み込み
    # 初期位置の読み込み
    s_i, s_j = map(int, input().strip().split())
    # タイル情報の読み込み
    tiles_list = []
    for i in range(H):
        row = list(map(int, input().strip().split()))
        tiles_list.append(row)
    tiles = np.array(tiles_list)
    # 点数情報の読み込み
    points_list = []
    for i in range(H):
        row = list(map(int, input().strip().split()))
        points_list.append(row)
    points = np.array(points_list)

    tile_id_set = set(tiles.flatten())
    used_tile_id_dict = {k: False for k in tile_id_set}

    score = 0

    # 初期位置の評価
    tile = int(tiles[s_i, s_j])
    used_tile_id_dict[tile] = True
    cur_i, cur_j = s_i, s_j

    best_scores = np.ones((H, W)) * (-1)
    best_score = 0

    q = [(0, cur_i, cur_j, "", set([int(tiles[s_i, s_j])]))]  # (score, i, j, actions, used_tiles)

    start = time.perf_counter()
    while time.perf_counter() - start < 1.5:
        if not q:
            break
        neg_score, current_i, current_j, actions, used_tiles = heapq.heappop(q)
        current_score = -neg_score
        if current_score > best_score:
            best_score = current_score
            best_actions = actions
        for di, dj, a in [(-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")]:
            ni, nj = current_i + di, current_j + dj
            if ni < 0 or ni >= H or nj < 0 or nj >= W:
                continue
            tile = int(tiles[ni, nj])
            if tile in used_tiles:
                continue
            bs = best_scores[ni, nj]
            new_score = current_score + points[ni, nj]
            if new_score < bs - 135:
                continue
            best_scores[ni, nj] = max(best_scores[ni, nj], new_score)
            new_actions = actions + a
            new_used_tiles = used_tiles | {tile}
            heapq.heappush(q, (-new_score, ni, nj, new_actions, new_used_tiles))

    print(best_actions)
    