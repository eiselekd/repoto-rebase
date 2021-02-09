#!python3
import os, re, json, time, copy, argparse, subprocess
from random import randrange
import shutil
from glob import glob
# apt install python-git
from git import Repo
# apt install python-flask
from flask import (
    Flask,
    request,
    render_template,
    send_from_directory
)
from repo.manifest import manifest, mh_project

cdir=os.path.dirname(os.path.abspath(__file__))

# git clone https://gitlab.com/noppo/gevent-websocket.git
from geventwebsocket.handler import WebSocketHandler
# git clone https://github.com/fgallaire/wsgiserver
from gevent.pywsgi import WSGIServer

parser = argparse.ArgumentParser(prog='dumpgen')
parser.add_argument('--verbose', action='store_true', help='verbose')
parser.add_argument('--prepare', action='store_true', help='verbose')
parser.add_argument('--a', '-a', type=str, default='test/manifest_test_a', help='repo manifest dir a')
parser.add_argument('--b', '-b', type=str, default='test/manifest_test_b', help='repo manifest dir b')
parser.add_argument('--workdir', '-w', type=str, default='/tmp/repo_work', help='work directory')
parser.add_argument('repos', nargs='*')
opt = parser.parse_args()

app = Flask(__name__, template_folder=".")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(cdir, path)

repodir=opt.a
workdir=opt.workdir; #"/tmp/repoto"
prepare_repobranch="master";
prepare_manifest="/data/repo/default.xml";


def update(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


@app.route('/api')
def api():
    global opt;
    global workdir;

    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        localprefix = "%08x"%(randrange(1<<30));
        print("New user %s" %(localprefix))
        base = os.path.join(workdir, localprefix)
        print("New user %s in '%s'" %(localprefix, base))
        # reset local dir
        try:
            shutil.rmtree(base)
        except:
            pass
        try:
            if not os.path.exists(base):
                os.makedirs(base)
        except:
            pass

        repolist = []

        while True:
            req = ws.read_message()
            print("Got '{}'".format(req))
            req = json.loads(req)
            print(str(req));
            if (req['type'] == 'start'):
                startobj = { };
                ws.send(json.dumps({'type': 'md', 'data' : [ update(startobj, {'repodir' : e }) for e in repolist]})) #opt.repos



            time.sleep(1);


if __name__ == '__main__':

    print ("Server localhost:5001/rebase.html")
    http_server = WSGIServer(('0.0.0.0',5001), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
