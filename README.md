# venv

この環境では venv でディレクトリ内のモジュールを管理しています

```
#仮想環境の有効化
$ source ~venv/bin/avtivate

#仮想環境の無効化
$ deactivate
```

# 認証情報や Discord 内の ID 格納用の.env ファイル作成

```
# discord.CodeWarehouse/python/のディレクトリに居ることを確認した上で.envファイル作成
touch .env

# .envの中身にBOTで使用するIDやTOKENなどのを記載済みの場合、サーバーで読み込む
source .env
```

### .env ファイルの中身

- 本番環境に配置している.env ファイル

```
###==============================
#Bot credential
# BOT TOKEN
###==============================
# プール監視員
DISCORD_BOT_TOKEN='{bot_token}'
# Cron
CRON_BOT_TOKEN='{bot_token}'
# 管理
MANAGER_BOT_TOKEN='{bot_token}'


###==============================
#Discord Guild
# SERVER ID
## CHANNEL ID
### CATEGORY ID
###==============================
# もくもくOnline勉強会
DISCORD_SEVER_ID={server_id}

## 勉強記録
DISCORD_CHANNEL_ID={channel_id}
## 勉強スロット当選者
SLOT_RESULT_CHANNEL_ID={channel_id}
## 週間勉強集計
WEEK_RECORD_CHANNEL_ID={channel_id}
## 月間勉強集計
MONTH_RECORD_CHANNEL_ID={channel_id}
## 参加・離脱ログ
JOIN_LEAVE_CHANNEL_ID={channel_id}
## 役職自動付与
AUTO_ROLE_CHANNEL_ID={channel_id}
## （初回）自己紹介
SELF_INTRODUCTION_CHANEL_ID={channel_id}

### ACTIVE_TIMES
ACTIVE_TIMES_CATEGORY_ID={category_id}
```

# Python のパッケージインストール

※requirements.txt がある場合

```
$ pip install -r requirements.txt
```

# Feature Description

- slot_studyrecord.py

```
 勉強記録ログにランダムで３個のリアクションを付与する
付与した結果に応じて指定した並びで出力された時
別のチャンネルに「大当たり」メッセージを出力する
```

## ファイルの説明

python/
┣ afk.py : 寝落ちした人を移動してサーバーミュートする機能
┣ PersonalPin.py : ギルド内のメッセージを自分の times にピン留めする機能
┣ slot_studyrecord.py : 勉強をするとランダムでスロットが周り、たまに大当たりする機能
┣ VCinvente.py : 今いる VC への招待リンクを対象の DM に送りつける機能
┣ management.py : Cogs/Managements 配下の機能を呼び出す・まとめて管理・実行する機能
┗ Cogs/
┣ default.py : Bot 起動時の on_ready のイベントをまとめたもの
┣ unmute.py :afk.py に呼び出され、サーバーミュートを解除する機能
┗ Managements/
┗ voiceChannelJoinLeave_roleModify.py : ラウンジと作業部屋の VC 参加時に対応したチャンネルを閲覧可能にする機能
