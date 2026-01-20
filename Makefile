.PHONY: install install-skills help

# デフォルトターゲット
help:
	@echo "使用可能なコマンド:"
	@echo "  make install        - すべての依存関係をインストール"
	@echo "  make install-skills - スキルの依存関係をインストール"

# すべての依存関係をインストール
install: install-skills

# スキルの依存関係をインストール
install-skills:
	@echo "スキルの依存関係をインストール中..."
	pip install -r .opencode/skills/gemini-drive/requirements.txt
	@echo "完了"
