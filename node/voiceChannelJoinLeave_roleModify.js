require("dotenv").config();

const Discord = require("discord.js");
const env = process.env;
const TOKEN = env.MANAGER_BOT_TOKEN;
const client = new Discord.Client();
const SERVER = env.DISCORD_SEVER_ID;

client.on("ready", () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

client.on("voiceStateUpdate", (before, after) => {
    const userid = after.id;
    const member = after.guild.members.cache.get(userid);

    // TODO: 2020/10/03 yabuta env等で定義できたらしたい。
    // 「作業部屋用チャット」表示権限ID
    const workRoomChatRoleId = "763401369784156211";
    // 「ラウンジ用チャット」表示権限ID
    const loungeChatRoleId = "763400537257148446";
    // 「作業部屋」ID
    const workRoomVoiceChatId = "683864874539024397";
    // 「ラウンジ」ID
    const loungeVoiceChatId = "603582455756095492";

    console.log("before: ", before.channelID, "(after) ", after.channelID);
    // 自分のギルドかつ、入室、退出の場合のみ
    if (after.guild.id === SERVER && before.channelID !== after.channelID) {
        console.log("viceStateUpdate");

        // ロール削除
        if(member.roles.cache.has(workRoomChatRoleId)){
            member.roles.remove(workRoomChatRoleId);
        }
        if(member.roles.cache.has(loungeChatRoleId)){
            member.roles.remove(loungeChatRoleId);
        }

        if (after.channelID == null) {
            // 退出
            console.log(
                `${member.user.username}(${userid})がボイスチャンネル から退室しました`
            );
            console.log(after.channel)
        } else if (before.channelID !== after.channelID) {
            // 入室 or 部屋変更
            console.log(
                `${member.user.username}(${userid})がボイスチャンネルに参加しました`
            );

            // 作業部屋に入室
            if (after.channelID === workRoomVoiceChatId) {
                member.roles.add(workRoomChatRoleId);
            }
            // ラウンジに入室
            if (after.channelID === loungeVoiceChatId) {
                member.roles.add(loungeChatRoleId);
            }
        }
    }
});

client.login(TOKEN);
