# 🏗️ CLAUDE.md - Claude Code グローバル設定

このファイルは、Claude Code (claude.ai/code) がすべてのプロジェクトで作業する際のガイダンスを提供します。

# Guidelines

This document defines the project's rules, objectives, and progress management methods. Please proceed with the project according to the following content.

## Top-Level Rules

- To maximize efficiency, **if you need to execute multiple independent processes, invoke those tools concurrently, not sequentially**.
- **You must think exclusively in English**. However, you are required to **respond in Japanese**.
- To understand how to use a library, **always use the Contex7 MCP** to retrieve the latest information.

## Programming Rules

- Avoid hard-coding values unless absolutely necessary.
- Do not use `any` or `unknown` types in TypeScript.
- You must not use a TypeScript `class` unless it is absolutely necessary (e.g., extending the `Error` class for custom error handling that requires `instanceof` checks).

### ドキュメントのテンプレート (Python)
```python
def function_name(param: ParamType) -> ReturnType:
    """関数の簡単な説明。
    
    関数が何を行い、なぜそれを行うのかについての詳細な説明。
    
    Args:
        param: パラメータの説明とその目的。
        
    Returns:
        返されるものとその構造の説明。
        
    Raises:
        ErrorType: この特定のエラー条件が発生する場合。
        
    Example:
        >>> result = function_name("input")
        >>> print(result)
        'expected output'
    """
    # 実装
```

### 基本ルール
- **discussion.mdを読む**: これまでの検証や実装については、discusion.mdの内容を読んで把握してください
- **pythonコマンドの実行**: **`uv`**でpythonを実行すること。直接`python`コマンドを使わないこと
- **パッケージマネージャー**: **`uv`を最優先で使用する。`pip`は直接使用しないこと
- **型ヒント**: すべての関数で必須 (`from __future__ import annotations` を活用)
- **非同期**: テストには`asyncio`ではなく`anyio`を使用する
- **行の長さ**: ruff.
- **テストの実行**: コードの修正後、tests内のテストコードを実行して全て成功することを確かめること
- **数式の表記**: mdファイル中で数式を記述する場合、GitHubのMarkdownの書式に従って記述してください
- **議論の保存**: 問題の解法について考えたことや、私と議論した内容はdiscussion.mdというファイルの中に記録しておいてください。また、解法について考える際にはまずdiscussion.mdの内容に目を通してください。