require("dotenv").config();

const Discord = require("discord.js");
const env = process.env;
const TOKEN = env.MANAGER_BOT_TOKEN;
const client = new Discord.Client({
  ws: {
    intents: Discord.Intents.ALL,
  }
});
const CHANNELID = env.SELF_INTRODUCTION_CHANEL_ID;
const categoryid = env.ACTIVE_TIMES_CATEGORY_ID;

const sendMessage = String.raw`
このチャンネルはあなたの分報(個人)チャンネルです。
使い方は「参考資料」又は「他メンバーの分報チャンネル」をご覧ください。
上手に活用してみてくださいね
 　参考資料：http://c16e.com/1511101558/
`;

const tutorialSendMessage = {
  embed: {
    color: 16757683,
    title: 'チュートリアル',
    description: '(※)既に完了している項目は飛ばしてください',
    thumbnail: {
      url: "https://mo9mo9study.github.io/discord.web/images/icon_logoBlackborder.png"
    },
    fields: [
      { name: ":one:",value: "自己紹介しよう" },
      { name: ":two:",value: "アイコン設定をしよう" },
      { name: ":three:",value: "ボイスチャット（ラウンジ、もくもく勉強机n）に参加して勉強を開始しよう" },
      { name: ":four:",value: "ボイスチャット（ラウンジ、もくもく勉強机n）に5分以上参加してから退席して、勉強記録をつけよう" },
      { name: ":five:",value: "今日の積み上げを確認してみよう「¥result_d」だけのメッセージを送信してみてね" },
      { name: ":six:",value: "昨日の勉強記録は「¥result_d ago」だけのメッセージを送信してみてね" },
      { 
        name: ":tada: 全チュートリアル完了した方へ", 
        value: "お疲れ様です。timesという個人チャンネルについては他の人のtimesチャンネルをみて刺激もらったり、使い方を学んでみよう！",
        inline: true
      },
      {
        name: "🔰 チュートリアルの進捗管理",
        value: "このメッセージの下にチュートリアルの数だけ対応するスタンプを付与していますので、クリアしたらスタンプを押して進捗を管理してみてください。",
        inline: true
      }
    ]
  }
}

const allChannelNameList = (values) => {
  const list = [];
  values.map((value) => {
    if (!value.type.includes("text")) return;
    if (value.name.includes("times_")) {
      list.push(value.name);
    }
  });
  return list;
};

client.on("ready", () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on("message", (message) => {
  if (message.channel.id != CHANNELID) return;
  const channels = allChannelNameList(message.channel.guild.channels.cache);
  const channelName = ("times_" + message.author.username).toLowerCase();
  console.log(`timesチャンネルは${channels.length}個存在します`);
  //if (message.content.includes("呼び名")) {
  if (channels.includes(channelName)) {
    console.log("既にチャンネル名が存在します");
  } else {
    if (channels.length > 50) {
      let alertMessage = `timesチャンネルが50個(現在：${channels.length}個)を超えました`;
      // 管理者の文法チャンネルにメンション付きで連絡する機能
      const member = message.channel.guild.members.cache.get(
        message.channel.guild.ownerID
      );
      // おいおいは、チャンネルのトピックにownerIDが含まれているチャンネルを選択するやり方にする
      const channel = message.channel.guild.channels.cache.get(
        "673006702924136448"
      );
      channel
        .send(alertMessage, { reply: member })
        .then(
          console.log(
            `${channel.name}に「分報チャンネル」の総数が50個を超えた旨を連絡しました`
          )
        )
        .catch(console.error);
    }
    message.channel.guild.channels.create(channelName, {
      type: "text",
      parent: categoryid,
      topic: message.author.id,
    });
    console.log(`${channelName}を作成しました`);
  }
  //}
});

client.on("channelCreate", async(channel) => {
  console.log(`---> 新しく[ ${channel.name} ]チャンネルが作成されました`);
  const channelUserid = channel.topic;
  const member = channel.guild.members.cache.get(channelUserid);
  console.log(member);
  if (member == undefined) return;
  if (channel.name.includes("times_")) {
    await channel
      .send(sendMessage, { reply: member })
      .then(
        console.log(
          `${channel.name}で${member.user.username}に「分報チャンネル」案内のメッセージを送りました`
        )
      )
      .catch(console.error);
      // チュートリアル
    sMessage = await channel
      .send(tutorialSendMessage)
      .then(
        console.log(
          `${channel.name}で${member.user.username}に「チュートリアル」メッセージを送りました`
        )
      )
      .catch(console.error);
    sMessage.react("1⃣")
    sMessage.react("2⃣")
    sMessage.react("3⃣")
    sMessage.react("4⃣")
    sMessage.react("5⃣")
    sMessage.react("6⃣")
  }
});

client.login(TOKEN);
