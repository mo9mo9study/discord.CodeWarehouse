# 目的
- Disocordギルド[ mo9mo9study ]でコミュ運営を便利にする機能を管理しています

# 起動方法
```sh
# venv
## この環境では venv でパッケージを管理しています
## 仮想環境の有効化
source venv/bin/avtivate
## 仮想環境の無効化する場合
# deactivate

# 認証情報や Discord 内の ID 格納用の.env ファイル作成
## discord.CodeWarehouse/python/のディレクトリに居ることを確認した上で.envファイル作成
cp .env.sample .env
vi .env # 必要な情報を入力

# pythonで使用するのパッケージインストール
pip install -r requirements.txt

#.pre-commit-config.yamlを適用してpre-commit時に自動コードレビューを行う設定適応
pre-commit install

## Cogs配下の各コードの中にチャンネルのIDを直接記入しているので
## 利用する際は各自のギルド内で使用するチャンネルIDに変更してください。
## また、management.pyから動かしたいコード以外をコメントすることで
## 必要な処理のみを動かすことが可能になる。

# 起動元のpythonファイルを起動する
python3 management.py
```
