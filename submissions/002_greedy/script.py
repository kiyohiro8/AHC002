
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
    score += points[s_i, s_j]
    tile = tiles[s_i, s_j]
    used_tile_id_dict[tile] = True
    cur_i, cur_j = s_i, s_j

    action_list = []

    while True:
        # 可能な行動をリストアップ
        possible_actions = []
        for di, dj, a in [(-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")]:
            ni, nj = cur_i + di, cur_j + dj
            if 0 <= ni < H and 0 <= nj < W:
                tile = tiles[ni, nj]
                if not used_tile_id_dict[tile]:
                    # ポイントも含めて保存
                    possible_actions.append((ni, nj, a, points[ni, nj]))

        if not possible_actions:
            break

        # 最も高いポイントを持つ行動を選択（貪欲法）
        best_action = max(possible_actions, key=lambda x: x[3])
        cur_i, cur_j, action, point_value = best_action
        score += point_value
        tile = tiles[cur_i, cur_j]
        used_tile_id_dict[tile] = True
        action_list.append(action)

    result = ''.join(action_list)
    print(result)