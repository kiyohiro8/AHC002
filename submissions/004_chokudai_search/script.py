# ビームサーチを用いた探索アルゴリズムの実装
import time
import heapq
import numpy as np

H, W = 50, 50

class Board:
    def __init__(self, tiles, points, cur_i, cur_j, used_tile_id_dict, actions, score=0):
        self.tiles = tiles
        self.points = points
        self.cur_i = cur_i
        self.cur_j = cur_j
        self.used_tile_id_dict = used_tile_id_dict
        self.actions = actions
        self.score = score

    def get_legal_actions(self):
        legal_actions = []
        for di, dj, a in [(-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")]:
            ni, nj = self.cur_i + di, self.cur_j + dj
            if 0 <= ni < H and 0 <= nj < W:
                tile = int(self.tiles[ni, nj])
                if not self.used_tile_id_dict[tile]:
                    legal_actions.append((ni, nj, a, self.score + int(self.points[ni, nj])))
        return legal_actions

    def make_move(self, action):
        ni, nj, a, point_value = action
        return Board(
            self.tiles,
            self.points,
            ni,
            nj,
            {**self.used_tile_id_dict, int(self.tiles[ni, nj]): True},
            self.actions + [a],
            self.score + int(self.points[ni, nj])
        )

    def get_first_action(self):
        if self.actions:
            return self.actions[0]
        return None

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.score == other.score

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.score != other.score

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.score < other.score

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.score <= other.score

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.score > other.score

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.score >= other.score

def chokudai_search(initial_state, num_beams, beam_width=1, max_depth=200, limit=0.005):
    # Chokudaiサーチの実装
    beams = [[] for _ in range(max_depth + 1)]
    heapq.heappush(beams[0], (-initial_state.score, initial_state))
    best_state = initial_state
    start = time.perf_counter()

    for _ in range(num_beams):
        for depth in range(max_depth - 1):
            # ビーム幅に基づいてノードを展開
            for _ in range(beam_width):
                if not beams[depth]:
                    break
                current_score, current_state = heapq.heappop(beams[depth])
                legal_actions = current_state.get_legal_actions()
                #print(legal_actions)

                for action in legal_actions:
                    new_state = current_state.make_move(action)
                    heapq.heappush(beams[depth + 1], (-new_state.score, new_state))
                    if new_state.score > best_state.score:
                        best_state = new_state
            if time.perf_counter() - start > limit:
                break
        if time.perf_counter() - start > limit:
            break

    return best_state.get_first_action(), depth

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
    score += int(points[s_i, s_j])
    tile = int(tiles[s_i, s_j])
    used_tile_id_dict[tile] = True
    cur_i, cur_j = s_i, s_j

    state = Board(tiles, points, cur_i, cur_j, used_tile_id_dict, [])
    legal_actions = state.get_legal_actions()

    action_list = []
    start = time.perf_counter()
    while legal_actions:
        # ビームサーチを実行
        state.actions = []
        best_action, depth = chokudai_search(state, num_beams=3, beam_width=1, max_depth=1000, limit=0.005)
        if best_action is None:
            break

        action_list.append(best_action)
        if best_action is None:
            break
        elif best_action == "U":
            cur_i -= 1
        elif best_action == "D":
            cur_i += 1
        elif best_action == "L":
            cur_j -= 1
        elif best_action == "R":
            cur_j += 1
        score += int(points[cur_i, cur_j])
        tile = int(tiles[cur_i, cur_j])
        used_tile_id_dict[tile] = True
        # 次の状態を更新
        state = Board(tiles, points, cur_i, cur_j, used_tile_id_dict, [])
        legal_actions = state.get_legal_actions()

        if not legal_actions:
            break
        # 時間は1.5秒以内に制限し、ランダムな着手でプレイアウトを行う
        if time.perf_counter() - start > 1.5:
            # ランダムな着手でプレイアウト
            while legal_actions:
                action = legal_actions[np.random.choice(len(legal_actions))]
                state = state.make_move(action)
                action_list.append(action[2])
                legal_actions = state.get_legal_actions()
                if time.perf_counter() - start > 1.8:
                    break
            break

    result = ''.join(action_list)
    print(result)