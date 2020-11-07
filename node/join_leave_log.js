require("dotenv").config();
const Discord = require("discord.js");

const env = process.env;
const client = new Discord.Client();
const TOKEN = env.MANAGER_BOT_TOKEN;
const CHANNEL = env.JOIN_LEAVE_CHANNEL_ID;

const allInvites = {}

client.on("ready", async () => {
  client.guilds.cache.forEach(guild => {
    guild.fetchInvites().then(invites => {
      allInvites[guild.id] = invites
    })
  })
  console.log(`Logged in as ${client.user.tag}!`);
});

const sendMessage = (member, text) => {
  member.guild.channels.cache.get(CHANNEL).send(text);
};

client.on('inviteCreate', (invite) => {
  client.guilds.cache.forEach(guild => {
    guild.fetchInvites().then(invites => {
      allInvites[guild.id] = invites
    })
  })
  console.log("---> 招待作成")
});

client.on("guildMemberAdd", (member) => {
  console.log("---> 参加時");
  member.guild.fetchInvites().then(invites => {
    const oldInvites = allInvites[member.guild.id]
    allInvites[member.guild.id] = invites
    // 以前に取得した招待コードと新たに取得したので、使用回数が増えたものを探す
    const invite = invites.find(i => oldInvites.get(i.code).uses < i.uses)
    console.log(`${member.user.tag} は ${invite.code} を使ってサーバーに参加しました`)
    console.log(invite)
    if (invite.inviter.id) {
      console.log("---> url")
      var text = `${member.user.username} (__id:${member.user.id}__) が参加しました。【 招待者：<@${invite.inviter.id}> 】`;
    } else {
      console.log("---> id == null")
      var text = `${member.user.username} (__id:${member.user.id}__) が参加しました。【 参加元：https://mo9mo9study.github.io/discord.web/ 】`;
    }
    console.log("---> var/text: ",text)
    sendMessage(member, text);
  });
});

client.on("guildMemberRemove", (member) => {
  console.log("---> 離脱時");
  console.log(`${member.user.username} (__id:${member.user.id}__) が離脱しました。`);
  let text = `${member.user.username} (__id:${member.user.id}__) が離脱しました。`;
  sendMessage(member, text);
});

client.login(TOKEN);
