import argparse
from collections import defaultdict
import os
import subprocess
from typing import List, Tuple
import numpy as np
from tqdm import tqdm

H, W = 50, 50


def run_submission(script_path: str, input_file: str) -> Tuple[bool, List[str], str]:
    """提出スクリプトを実行する.
    
    Args:
        script_path: スクリプトのパス
        input_file: 入力ファイルのパス
        
    Returns:
        (成功フラグ, 出力行リスト, エラーメッセージ)
    """
    try:
        with open(input_file, 'r') as f:
            input_data = f.read()
        
        result = subprocess.run(
            ['uv', 'run', script_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=2
        )
        
        if result.returncode != 0:
            return False, [], f"実行エラー: {result.stderr}"
        
        output_lines = result.stdout.strip().split('\n')
        return True, output_lines[0], ""
        
    except subprocess.TimeoutExpired:
        return False, [], "TLE"
    except Exception as e:
        return False, [], f"実行エラー: {str(e)}"
    
def evaluate_output(output_line: str, input_file: str) -> int:
    """出力を評価する関数"""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    s_i, s_j = map(int, lines.pop(0).strip().split())

    tiles_list = []
    for _ in range(H):
        row = list(map(int, lines.pop(0).strip().split()))
        tiles_list.append(row)
    tiles = np.array(tiles_list)

    points_list = []
    for _ in range(H):
        row = list(map(int, lines.pop(0).strip().split()))
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
    for action in output_line:
        if action == 'U':
            cur_i -= 1
        elif action == 'D':
            cur_i += 1
        elif action == 'L':
            cur_j -= 1
        elif action == 'R':
            cur_j += 1

        if cur_i < 0 or cur_i >= H or cur_j < 0 or cur_j >= W:
            return score, "Out of bounds"
        next_tile = tiles[cur_i, cur_j]
        if used_tile_id_dict[next_tile]:
            return score, "Tile already used"
        score += points[cur_i, cur_j]
        used_tile_id_dict[next_tile] = True

    return score, "AC"


def evaluate_submission(
    script_path: str,
    input_file_dir: str,
) -> Tuple[bool, float, str]:
    """提出スクリプトを評価する.
    
    Args:
        script_path: 提出スクリプトのパス
        input_file: 入力ファイルのパス
        
    Returns:
        (成功フラグ, スコア, エラーメッセージ)
    """
    input_file_list = sorted(os.listdir(input_file_dir))
    output_dir = os.path.dirname(script_path)
    output_path = os.path.join(output_dir, "evaluate.csv")
    results = []

    for input_file in input_file_list:
        success, output_line, error_message = run_submission(script_path, os.path.join(input_file_dir, input_file))

        if not success:
            print(f"Error in {input_file}: {error_message}")

        score, message = evaluate_output(output_line, os.path.join(input_file_dir, input_file))
        print(f"{input_file}: {score}, {message}")
        results.append((input_file, score, message))

    # 結果をCSVファイルに保存
    with open(output_path, 'w') as f:
        for input_file, score, message in results:
            f.write(f"{input_file},{score},{message}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a submission script.")
    parser.add_argument('script_path', type=str, help='Path to the submission script.')
    parser.add_argument('input_file_dir', type=str, help='Directory containing input files.')
    args = parser.parse_args()


    script_path = args.script_path
    input_file_dir = args.input_file_dir

    evaluate_submission(script_path, input_file_dir)

