@app.route('/all/myipinit')
def myip():
  if 'token' in request.args:
    if re.findall(r'(AppleWebKit|Chrome|Safari|KHTML|Gecko)', request.headers.get('User-Agent')):
      token = re.fullmatch(r'[A-Za-z0-9]+', request.args['token']).string
      output = bash('FROM=API /var/cld/modules/access/bin/cld-activateiptoken '+vld(remoteaddr())+' '+token)
      resp = Response(output, status=200, mimetype='text/plain')
      return resp
    else:
      return Response('403', status=403, mimetype='text/plain')
  else:
    return Response('403', status=403, mimetype='text/plain')

@app.route('/myvpninit')
def myvpninit():
  if 'token' in request.args:
    if re.findall(r'(AppleWebKit|Chrome|Safari|KHTML|Gecko)', request.headers.get('User-Agent')):
      token = re.fullmatch(r'[A-Za-z0-9]+', request.args['token']).string
      text = 'CLD VPN key generating...'
      link = f'/api/myvpnget?token={token}'
      render_template('modules/access/preloader.html', text=text, link=link)
    else:
      return Response('403', status=403, mimetype='text/plain')
  else:
    return Response('403', status=403, mimetype='text/plain')

@app.route('/myvpnget')
def myvpnget():
  if 'token' in request.args:
    if re.findall(r'(AppleWebKit|Chrome|Safari|KHTML|Gecko)', request.headers.get('User-Agent')):
      token = re.fullmatch(r'[A-Za-z0-9]+', request.args['token']).string
      filepath = bash('FROM=API /var/cld/modules/access/bin/cld-activatevpntoken '+token)
      if os.path.exists(filepath) != True:
        return Response('404', status=404, mimetype='text/plain')
      filename = os.path.basename(filepath)
      resp = Response(stream_file(filepath), status=200, mimetype='application/octet-stream')
      resp.headers['Content-Disposition'] = "attachment; filename="+filename
      return resp
    else:
      return Response('403', status=403, mimetype='text/plain')
  else:
    return Response('403', status=403, mimetype='text/plain')