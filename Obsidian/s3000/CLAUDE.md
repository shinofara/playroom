# s3000 - Obsidian Vault

## プロジェクト概要

playroomモノレポ内のObsidian Vaultサブプロジェクト。

## 基本方針

- コメントやターミナルへの出力は日本語とする
- Obsidianのノート管理に関する作業を支援する

## Git ワークフロー

### ブランチ管理
- ブランチ作成時は `claude/<name>_YYYYMMDDHimm` フォーマットとする

### コミット管理
- git commitは意味のある作業単位で行う

### プッシュとプルリクエスト
- git pushする前にdefaultブランチをpull rebaseする
- pushしたらPRのURLを表示し、openコマンドで開く
