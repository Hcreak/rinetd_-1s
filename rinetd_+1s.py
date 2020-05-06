#!/bin/env python
# _*_coding:utf-8_*_
import os
from flask import *
import random
import csv
import compute_log

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

# logs part
#############
@app.route('/logs', methods=['GET'])
def shit1():
    if os.path.exists('/rinetd_+1s/iplog.csv'):
        l = []
        with open('/rinetd_+1s/iplog.csv','r') as f: 
            reader = csv.reader(f)
            for row in reader:
                # print row
                l.append(row)
        for i in l[1:]:
            i[4] = i[4].decode('utf-8')
        return render_template('logs.html', gen_time=l[0][5], itemlist=l[1:])
    else:
        return render_template('logs.html', gen_time='NULL', itemlist=[['null','null','null','null','null']])

@app.route('/logs_compute', methods=['POST'])
def shit2():
    outdata = compute_log.main()
    compute_log.csvout(outdata)
    return 'finally'

@app.route('/logs_compute', methods=['GET'])
def shit3():
    return jsonify(compute_log.reportcur())

@app.route('/logs_csv', methods=['GET'])
def shit4():
    return send_file('iplog.csv', mimetype='text/csv', as_attachment=True, attachment_filename='iplog.csv')

@app.route('/logs_source', methods=['GET'])
def shit5():
    return send_file('rinetd.log', mimetype='text/plain', as_attachment=True, attachment_filename='rinetd.log')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)