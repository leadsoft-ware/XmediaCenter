from types import CodeType
import flask,core.plugins.FileManager.file_manage,core.api,core.xmcp,os
from flask.globals import g
from flask.templating import render_template
import json

name = 'BilibiliVideosDownloader'

requestCPR = None

def cross_plugin_request(args:list):
    return 'denied'

def get_plugins_path_list():
    ret = []
    #print(requestCPR())
    for i in requestCPR():
        if i.name == name:
            continue
        path = i.cross_plugin_request([ 'get_path' ])
        if type(path).__name__ == 'str' and path == 'denied':
            pass
        else:
            ret.append([path,i.name])
    return ret

def api_request(request:flask.request):
    request_path = request.values.get('path')
    url = request.values.get('url')
    if url != None and url[0] == '"':
        url = url[1:-1]
    cookies = ' '
    if os.access(os.getcwd()+'/core/plugins/BilibiliVideosDownloader/cookies.sqlite',os.F_OK):
        cookies = ' --cookies "' + os.getcwd()+'/core/plugins/BilibiliVideosDownloader/cookies.sqlite' + '" '
    print("cmd:",'~/.local/bin/you-get -l ' + url + ' -o "' + os.getcwd() + '/core/storage/' + request_path + '"' + cookies)
    fp = os.popen('~/.local/bin/you-get -l ' + url + ' -o "' + os.getcwd() + '/core/storage/' + request_path + '"' + cookies,'r')
    str = ''
    while True:
        str = fp.readline()
        if str == '':
            break
        str = str.replace('\n','')
        print(str,end='')
        for i in str:
            print('\b',end='')
        print('\b',end='')
    fp.close()
    return json.dumps({'status':'success'})

def register(server:flask.Flask):
    return {
        'registered_api': ['vd_api']
    }