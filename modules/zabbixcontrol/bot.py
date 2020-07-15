def allowzbxgroups():
  return set(bash("grep ALLOW_DNS_GROUP_IDS /var/cld/creds/creds_security_system | cut -d = -f 2").strip().split(','))

@bot.message_handler(commands=["webcheck"])
def cmd_webcheck(message):
   valid_id = str(message.chat.id)
   valid_id2 = str(message.from_user.id)
   if valid_id in allowzbxgroups() or valid_id2 in allowusers():
     if re.findall(r'([a-z0-9.*-]+\.[a-z0-9.-]+)(\s+?[A-Za-z0-9.*:@\/?&= -]+)?', message.text):
        zbxargs = re.search('([a-z0-9.*-]+\.[a-z0-9.-]+)(\s+?[A-Za-z0-9.*:@\/?&= -]+)?', message.text)
        zbxhost = zbxargs.group(1)
        zbxothers = ''
        try:
          zbxothers = str(zbxargs.group(2)).replace('None', '')
        except:
          pass
        cmdoutput = bash('/var/cld/modules/zabbixcontrol/bin/cld-zbxwebcheck '+str(zbxhost)+' '+str(zbxothers))
        bot.send_message(message.chat.id, cmdoutput, parse_mode='Markdown')
     else:
        bot.send_message(message.chat.id, text="web host is not defined, please use format:\n`/webcheck example.com -pattern=testword -url=https://examlpe.com/test?test=test`", parse_mode='Markdown')
   else:
      myid_answer = "user id is %s, access denied for %s" % (message.from_user.id, message.from_user.username)
      bot.send_message(message.chat.id, myid_answer)