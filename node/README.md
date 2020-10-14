# Node.jsのパッケージインストール
※packege.jsonがある場合
```
$ npm install
```

# Feature Description
- activetimes_move.js
> 個人のtimes内でメッセージが送信された時、
> 分報カテゴリーからACTIMEのカテゴリーにtimesが移動する
> AM2時に定期実行でACTIVEのカテゴリーから分報カテゴリーに戻す処理

- autoCreateTimes.js
```
自己紹介チャンネルで
「呼び名」というメッセージを含んだ自己紹介メッセージを送信すると
送信者のtimesが存在しない場合のみtimesを作成する
```
- join_leave_log.js 
```
参加者が既存メンバーの誰が作成した招待URLで参加したかを把握するために
参加時のログと共にURL作成者にメンションが飛ぶ
退室時は特に代わり映えもなく誰が退室したかを出力する

```
- rolesmaneger.js
```
RSSカテゴリー配下の各チャンネル＋gymチャンネルの閲覧権限を付与される
「A」から始まるアルファベットのリアクションを押すことで
メッセージより対応したチャンネルが閲覧できるようになる
```
- voiceChannelJoinLeave_roleModify.js
```
作業部屋とラウンジの各専用チャットが
対応するVC参加時のみ表示されるようにする
```
