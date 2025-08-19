# AHC002 - AtCoder Heuristic Contest 002

AtCoder Heuristic Contest 002（Walking on Tiles）を題材に、ヒューリスティックアルゴリズムを学習・実装するためのリポジトリです。

## 問題概要

50×50のグリッド上で、各マスには以下の2つの情報があります：
- **タイルID**: 同じタイルIDのマスは一度しか通れない
- **得点**: そのマスを通過したときに獲得できるポイント

初期位置から開始し、上下左右に移動しながら、同じタイルを2度踏まないように移動して、できるだけ多くの得点を獲得することが目標です。

## プロジェクト構造

```
AHC002/
├── inputs/              # 100個のテストケース（0000.txt～0099.txt）
├── submissions/         # 各解法の実装
│   ├── 001_sample_random/     # ランダム選択による解法
│   ├── 002_greedy/            # 貪欲法による解法
│   ├── 003_beam_search/       # ビームサーチによる解法
│   ├── 004_chokudai_search/   # Chokudaiサーチによる解法
│   └── 005_bfs/               # 幅優先探索+動的計画法による解法
├── evaluator.py         # 提出スクリプトの評価用プログラム
├── pyproject.toml       # プロジェクト設定（uvによる依存関係管理）
└── CLAUDE.md           # Claude Code用の設定ファイル

```

## 実装された解法

### 1. ランダム選択（001_sample_random）
- 移動可能な方向からランダムに選択
- ベースラインとなる最も単純な実装

### 2. 貪欲法（002_greedy）
- 各ステップで移動可能な隣接マスのうち、最も得点が高いマスを選択
- シンプルだが局所最適解に陥りやすい

### 3. ビームサーチ（003_beam_search）
- 複数の経路を同時に探索し、各深さで上位k個の状態のみを保持
- 貪欲法より広い探索空間をカバー

### 4. Chokudaiサーチ（004_chokudai_search）
- 時間制限内で深さ優先的にビームサーチを繰り返す手法
- AtCoderのchokudai氏により考案されたアルゴリズム

### 5. 幅優先探索（005_bfs）
- BFS+動的計画法っぽいアルゴリズム
- https://qiita.com/c-yan/items/cbba8249e248cc63736c で紹介されていた解法。

## セットアップ

```bash
# uvをインストール（まだの場合）
pip install uv

# 依存関係のインストール
uv sync
```

## 使用方法

### 個別の解法を実行
```bash
# 例：貪欲法を単一のテストケースで実行
uv run submissions/002_greedy/script.py < inputs/0000.txt
```

### 全テストケースで評価
```bash
# 例：貪欲法を全100ケースで評価
uv run python evaluator.py submissions/002_greedy/script.py inputs/
```

評価結果は各submissionディレクトリ内の`evaluate.csv`に保存されます。

