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
from repo.git import getRepoDir, getRepo, listOfRepoBranches, gatherRefs, repodiff, repocommit

cdir=os.path.dirname(os.path.abspath(__file__))

# git clone https://gitlab.com/noppo/gevent-websocket.git
from geventwebsocket.handler import WebSocketHandler
# git clone https://github.com/fgallaire/wsgiserver
from gevent.pywsgi import WSGIServer

parser = argparse.ArgumentParser(prog='dumpgen')
parser.add_argument('--verbose', action='store_true', help='verbose')
parser.add_argument('--prepare', action='store_true', help='verbose')
parser.add_argument('--workdir', '-w', type=str, default='/tmp/repo_work', help='work directory')
parser.add_argument('repos', nargs='*')
opt = parser.parse_args()

app = Flask(__name__, template_folder=".")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(cdir, path)

workdir=opt.workdir; #"/tmp/repoto"


for r in opt.repos:
    getRepoDir(workdir, r);

def update(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

selobj_ar = ['repodir', 'id', 'branches', 'srcbranch', 'srctag', 'dstbranch', 'shacommit' ];
class selobj:

    def __init__(self,v):
        global selobj_ar;
        self.v = v;
        for a in selobj_ar:
            if a in v:
                print(" > Select {}: '{}'".format(a,v[a]));

    def __getattr__(self, n):
        if n in self.v:
            return self.v[n]
        return None

    def tohash(self):
        global selobj_ar;
        r = {};
        for a in selobj_ar:
            if a in self.v and not (self.v[a] is None):
                r[a] = self.v[a];
        return r;

    def __str__(self):
        return repr(self.tohash());


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
                ws.send(json.dumps({'type': 'repolist', 'data' : [ update(startobj, {'repodir' : e }) for e in opt.repos]}))
            else:
                d = selobj(req['data'])
                if (req['type'] == 'reposel'):
                    r = getRepo(workdir, d.repodir);
                    b = listOfRepoBranches(r, '(.*)');
                    a = gatherRefs(r);
                    ws.send(json.dumps({'type': 'branchlist', 'data' : update(d.tohash(), {'branches' : sorted(b), 'tags' : sorted(b + a ) }) }))
                elif (req['type'] == 'getpatchlist'):
                    r = getRepo(workdir, d.repodir);
                    add = repodiff(r, req['data']['srctag'], req['data']['srcbranch']);
                    ws.send(json.dumps({'type': 'patchlist', 'data' : update(d.tohash(), {'patches' : add })}));
                elif (req['type'] == 'getcommit'):
                    r = getRepo(workdir, d.repodir);
                    try:
                        c = repocommit(r, req['data']['shacommit']);
                        ws.send(json.dumps({'type': 'commit', 'data' : update(d.tohash(), c)}));
                    except Exception as e:
                        print(str(e));
                elif (req['type'] == 'updatepatchlist'): # used to store persistent presets
                    pass
                elif (req['type'] == 'sendpatchlist'):
                    pass

            time.sleep(1);


if __name__ == '__main__':

    print ("Server localhost:5001/rebase.html")
    http_server = WSGIServer(('0.0.0.0',5001), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
