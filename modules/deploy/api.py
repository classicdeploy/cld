import hashlib
@app.route("/deploy/<deploytype>/<deploy>/<file>")
def deploy_get_file(deploytype, deploy, file):
    apihash = request.args['hash']
    for line in open('/var/cld/creds/passwd').read().strip().split('\n'):
      token = line.split(':')[2]
      checkhash = hashlib.md5(str(deploytype+deploy+file+token).encode('utf-8')).hexdigest()
      print(token+" "+checkhash+" "+apihash, flush=True)
      if checkhash == apihash:
        user = line.split(':')[0]
        break
    try: user
    except: return Response("404", status=403, mimetype='text/plain')
    checkresult = checkpermswhiteip(cldmodule, "NONE", token,  remoteaddr())
    if checkresult[0] != "granted": return Response("403", status=403, mimetype='text/plain')
    user = userbytoken(checkresult[1])
    user = str(re.match('^[A-z0-9.,@=/_ -]+', user)[0])
    user_allowed_deploys = json.loads(bash('sudo -u '+user+' sudo FROM=CLI /var/cld/modules/deploy/bin/cld-deploy --list --json'))
    if deploytype == "templates":
        deploys = user_allowed_deploys[0]['content']
    elif deploytype == "deploys":
        deploys = user_allowed_deploys[1]['content']
    if deploy in deploys:
        return Response(open('/var/cld/modules/deploy/'+deploytype+'/'+deploy+'/'+file).read(), status=200, mimetype='text/plain')
    else:
        return Response(deploytype[:-1].capitalize()+" not found", status=404, mimetype='text/plain')