# -*- coding: utf-8 -*-
from flask import Flask
from flask import abort, request
import requests
from flask import g
from flask import Response
import json
import re
import subprocess
import random
import datetime
from urllib.request import urlopen
import os

def customattr(s,n,v):
  class a(type(s)):
    def ttr(self,n,v):
      setattr(self,n,v)
      return self
  return a(s).ttr(n,v)

def bash(cmd):
  initproc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable='/bin/bash')
  return customattr(initproc.communicate()[0].decode('utf8').strip(), 'status', initproc.returncode)

def vld(cld_variable):
  return re.match('(^[A-z0-9.,@=/_ -]+?$|^$)', cld_variable).string

ansifiltercheck = bash('which ansifilter &>/dev/null && echo 0 || echo 1')
if ansifiltercheck == "0":
  outputinterpreter = bash('which ansifilter')
else:
  outputinterpreter = bash('which cat')
  print("ansifilter IS NOT INSTALLED IN THE SYSTEM - API OUTPUT WILL NOT FILTERED - https://github.com/andre-simon/ansifilter")

def stream_file(filepath, chunksize=8192):
  with open(filepath, "rb") as f:
    while True:
      chunk = f.read(chunksize)
      if chunk:
        yield chunk
      else:
        break

def bashstream(cmd, format="plain"):
  addopentag = ""
  addclosetag = ""
  outputargs = ""
  if format == "html" and ansifiltercheck == "0":
    outputargs = " -Hf"
    addopentag = "<pre>"
    addclosetag = "</pre>"
  elif format == "plain" and ansifiltercheck == "0":
    outputargs = " -Tf"
  process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable='/bin/bash')
  yield ''.join(addopentag)
  for line in process.stdout:
    yield ''.join(bash("echo -e $(cat << 'EOHTML' | "+outputinterpreter+outputargs+os.linesep+line.decode('utf8')+os.linesep+"EOHTML"+os.linesep+")")+'\n')
  yield ''.join(addclosetag)

def remoteaddr():
  if request.headers.getlist("X-Forwarded-For"):
    remote_addr = request.headers.getlist("X-Forwarded-For")[0]
  else:
    remote_addr = request.remote_addr
  return re.match("[A-z0-9.:]+", remote_addr)[0]

def accesslist():
  return bash('cat /var/cld/api/accesslist').split('\n')

def allowmoduleusers(cldmodule):
  return set(bash('''awk -F ":" '{print $3":"$4}' /var/cld/creds/passwd | grep "'''+vld(cldmodule)+'''\|ALL" | cut -d : -f 1''').split('\n'))

def allowutilityusers(cldutility):
  return set(bash('''awk -F ":" '{print $3":"$5}' /var/cld/creds/passwd | grep "'''+vld(cldutility)+'''\|ALL" | cut -d : -f 1''').split('\n'))

def checkperms(cldmodule, cldutility, token):
  token=re.match("[A-z0-9_.-]+", token)[0]
  cldmodule=str(cldmodule)
  cldutility=str(cldutility)
  if token in allowmoduleusers(cldmodule) or token in allowutilityusers(cldutility):
    return ["granted", token]
  else:
    return ["denied", "DENIED"]

def checkpermswhiteip(cldmodule, cldutility, token, remoteaddr):
  token=re.match("[A-z0-9_.-]+", token)[0]
  cldmodule=str(cldmodule)
  cldutility=str(cldutility)
  if token in allowmoduleusers(cldmodule) and remoteaddr in accesslist():
    return ["granted", token]
  elif token in allowutilityusers(cldutility) and remoteaddr in accesslist():
    return ["granted", token]
  else:
    return ["denied", "DENIED"]

def userbytoken(token):
  return bash('grep ":'+vld(token)+':" /var/cld/creds/passwd | cut -d : -f 1 | head -1')

cld_domain = bash('''grep CLD_DOMAIN /var/cld/creds/creds | cut -d = -f 2 | tr -d '"' ''')
telegram_bot_token = bash('''grep TELEGRAM_BOT_TOKEN /var/cld/creds/creds | cut -d = -f 2 | tr -d '"' ''')
app = Flask(__name__)

cldm={}
for apifile in bash("ls /var/cld/modules/*/api.py").split('\n'):
  cldmodule=bash('echo '+vld(apifile)+' | rev | cut -d / -f 2 | rev')
  cldm[cldmodule]=cldmodule
  print(cldmodule)
  exec(open(apifile).read().replace('cldmodule', 'cldm["'+cldmodule+'"]'))

exec(bash('''
for CLD_FILE in $(find /var/cld/bin/ /var/cld/modules/*/bin/ -type f -maxdepth 1 -name 'cld*')
do
CLD_MODULE=$(rev <<< ${CLD_FILE} | cut -d / -f 3 | rev)
CLD_UTIL=$(rev <<< ${CLD_FILE} | cut -d / -f 1 | rev)
cat << EOL
@app.route('/${CLD_UTIL/cld-/}')
def cmd_${CLD_UTIL//[.-]/_}():
    checkresult = checkpermswhiteip("${CLD_MODULE}", "${CLD_UTIL}", request.args['token'], remoteaddr()) 
    if checkresult[0] != "granted": return Response("403", status=403, mimetype='application/json')
    user = userbytoken(request.args['token'])
    output = 'plain'
    try: output = str(re.match('^[a-z]+$', request.args['output']).string)
    except: pass
    cmd_args = ''
    try: cmd_args = str(re.match('^[A-z0-9.,@=/: -]+$', request.args['args']).string)
    except: pass
    tgout = ''
    try: tgout = ' | /var/cld/modules/telegramcloud/bin/cld-tcloud-stream --chatid='+vld(request.args['tgout'])
    except: pass
    bg = ''
    try: 
      if str(int(request.args['bg'])) == '1': bg = ' &>/dev/null &'
    except: pass
    mode = 'stream'
    try: mode = str(re.match('^[a-z]+$', request.args['mode']).string)
    except: pass
    print('sudo -u '+user+' sudo FROM=API ${CLD_FILE} '+cmd_args+bg, flush=True)
    if mode == "track":
      cmdoutput = bash('sudo -u '+user+' sudo FROM=API '+vld("${CLD_FILE}")+' '+cmd_args+tgout+bg)
      if cmdoutput.status == 0:
        respstatus = 200
      else:
        respstatus = 500
      return Response(cmdoutput, status=respstatus, mimetype='text/plain')
    else:
      return Response(bashstream('sudo -u '+user+' sudo FROM=API '+vld("${CLD_FILE}")+' '+cmd_args+tgout+bg, output), status=200, mimetype='text/'+output)

EOL
done
'''))

@app.route('/all/ip')
def index():
  return remoteaddr()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8085)
