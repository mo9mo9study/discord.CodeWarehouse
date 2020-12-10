- 現在 js のコードを順次 python に移行中

# Node.js のパッケージインストール

※packege.json がある場合

```
$ npm install
```

# 認証情報や Discord 内の ID 格納用の.env ファイル作成

```
# discord.CodeWarehouse/node/のディレクトリに居ることを確認した上で.envファイル作成
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

# Feature Description

- activetimes_move.js

---

```
個人のtimes内でメッセージが送信された時、
分報カテゴリーからACTIMEのカテゴリーにtimesが移動する
AM2時に定期実行でACTIVEのカテゴリーから分報カテゴリーに戻す処理
```

- autoCreateTimes.js

---

```
自己紹介チャンネルで
「呼び名」というメッセージを含んだ自己紹介メッセージを送信すると
送信者のtimesが存在しない場合のみtimesを作成する
```

- join_leave_log.js

---

```
参加者が既存メンバーの誰が作成した招待URLで参加したかを把握するために
参加時のログと共にURL作成者にメンションが飛ぶ
退室時は特に代わり映えもなく誰が退室したかを出力する

```

- rolesmaneger.js

---

```
RSSカテゴリー配下の各チャンネル＋gymチャンネルの閲覧権限を付与される
「A」から始まるアルファベットのリアクションを押すことで
メッセージより対応したチャンネルが閲覧できるようになる
```
