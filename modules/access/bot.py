@bot.message_handler(commands=["myip"])
def cmd_myip(message):
  checkresult = checkperms(cldmodule, "myip", message.from_user.id, message.chat.id, message.from_user.username)
  if checkresult[0] != "granted": return
  user = bash('grep ":'+checkresult[1]+':" /var/cld/creds/passwd | cut -d : -f 1 | head -1 | tr -d "\\n"')
  if re.findall(r'[\d]+\.[\d]+\.[\d]+\.[\d]+', message.text):
    myip = re.search('([\d]+\.[\d]+\.[\d]+\.[\d]+)', message.text).group(1)
    cmdoutput = bash('sudo -u '+user+' sudo FROM=BOT /var/cld/modules/access/bin/myip '+str(message.from_user.id)+' '+str(message.from_user.username)+' '+str(myip))
    bot.send_message(message.chat.id, cmdoutput, parse_mode='Markdown')
  else:
    myip = 'TOKEN'
    cmdoutput = bash('sudo -u '+user+' sudo FROM=BOT /var/cld/modules/access/bin/myip '+str(message.from_user.id)+' '+str(message.from_user.username)+' '+str(myip))
    bot.send_message(message.chat.id, cmdoutput, parse_mode='Markdown', disable_web_page_preview='true')