# Cogsフォルダについて
CogsフォルダはCogファイルをまとめるフォルダです

## ディレクトリ[Managements]
- management.pyから起動される
- pypiからインストールできるdiscord.pyのバージョン1.7を想定して作成されたbot処理

## ディレクトリ[Managements-v2]
- management-v2.pyから起動される
- スレッド機能に対応するため、githubから直接discord.pyのv2.0.0aインストールし動かすbot処理
自times以外のメッセージを自timesにピン留めする機能をスレッドにも対応させるため、処理（venv環境）を別にするためManagementsと分裂

## ディレクトリ[afk]
- management.pyから起動される
- 寝落ちしてしまった人をAFK用のチャンネルに移動し、サーバー側ミュートを適用させる

## ファイル[default.py]
- management.py/management-v2.pyから起動される
- 全てのスクリプトで同じ処理をする場合に使用します。
例: on_readyイベントでprintしたい文字列を全て同じにする場合
