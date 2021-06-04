# 目的
- Disocordギルド[ mo9mo9study ]でコミュ運営を便利にする機能を管理しています

# 起動方法
```sh
# venv
## この環境では venv でパッケージを管理しています
## 仮想環境の有効化
source venv/bin/avtivate
##仮想環境の無効化
deactivate

# 認証情報や Discord 内の ID 格納用の.env ファイル作成
## discord.CodeWarehouse/python/のディレクトリに居ることを確認した上で.envファイル作成
cp .env.sample .env
vi .env # 必要な情報を入力

# pythonで使用するのパッケージインストール
pip install -r requirements.txt

# 起動元のpythonファイルを起動する
python3 management.py
```
