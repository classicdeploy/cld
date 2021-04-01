webmodule["deploy"] = {}
webmodule["deploy"]["homename"] = "Deploy"
webmodule["deploy"]["desc"] = "Classic deploy"
@app.route("/deploy")
def deploy_index():
  if 'username' in session:
    user = session['username']
    checkresult = checkpermswhiteip(cldmodule, 'NOTOOL', user, remoteaddr())
    if checkresult[0] != "granted": return Response("403", status=403, mimetype='application/json')
    deploys = json.loads(bash('sudo -u '+user+' sudo FROM=CLI /var/cld/deploy/bin/cld-deploy --list --json'))
    return render_template('modules/deploy/deploy.html', username=user, deploys=deploys)

@app.route("/deploy/<deploytype>/<deploy>")
def deploy_files(deploytype, deploy):
  if 'username' in session:
    user = session['username']
    checkresult = checkpermswhiteip(cldmodule, 'NOTOOL', user, remoteaddr())
    if checkresult[0] != "granted": return Response("403", status=403, mimetype='application/json')
    return Response(json.dumps(bash('{ DEPLOY_FILES=$(ls /var/cld/deploy/'+deploytype+'/'+deploy+') ; for CLD_FILE in vars script clouds ; do grep -s "^$CLD_FILE" <<< "$DEPLOY_FILES" ; done ; grep -v "^vars\|^script\|^clouds" <<< "$DEPLOY_FILES" ; }').split('\n')), status=200, mimetype='application/json')

@app.route("/deploy/templates/<template>/<file>")
def deploy_template_file(template, file):
  if 'username' in session:
    user = session['username']
    checkresult = checkpermswhiteip(cldmodule, 'NOTOOL', user, remoteaddr())
    if checkresult[0] != "granted": return Response("403", status=403, mimetype='application/json')
    return Response(bash('cat /var/cld/deploy/templates/'+template+'/'+file), status=200, mimetype='text/plain')

@app.route("/deploy/deploys/<deploy>/<file>")
def deploy_deploy_file(deploy, file):
  if 'username' in session:
    user = session['username']
    checkresult = checkpermswhiteip(cldmodule, 'NOTOOL', user, remoteaddr())
    if checkresult[0] != "granted": return Response("403", status=403, mimetype='application/json')
    return Response(bash('cat /var/cld/deploy/deploys/'+deploy+'/'+file), status=200, mimetype='text/plain')