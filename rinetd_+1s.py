#!/bin/env python
# _*_coding:utf-8_*_
import os
from flask import *
import random

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    out1 = os.popen('cat /rinetd_+1s/rinetd.conf').read()
    out2 = os.popen('netstat -tulnp|grep rinetd').read()
    out3 = os.popen('firewall-cmd --list-all').read()
    return render_template('+1s.html', rinetd=out1, netstat=out2, firewall=out3)

@app.route('/', methods=['POST'])
def shit():
    try:
        if os.path.exists('/run/rinetd.pid'):
            pid = os.popen('cat /run/rinetd.pid').read()
            os.popen('kill {}'.format(pid))
        random_port = random.randint(40000, 60000)
        os.popen('/rinetd_+1s/make_rinetd.sh {} {}'.format(str(random_port), str(random_port+10)))
        os.popen('/usr/sbin/rinetd -c /rinetd_+1s/rinetd.conf')
        os.popen('firewall-cmd --reload')
        os.popen('firewall-cmd --add-port={}-{}/tcp'.format(str(random_port), str(random_port+10)))
    except:
        return '0'
    return '1'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)