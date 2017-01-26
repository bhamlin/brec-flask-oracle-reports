#!/usr/bin/python3

import os
import sys

# os.environ['ORACLE_HOME'] = '/usr/lib/oracle/11.2/client64'
# os.environ['TNS_ADMIN'] = '/usr/lib/oracle/11.2/client'
# os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'

os.environ['FLASK_ORACLE_CONFIG'] = '/etc/flask_oracle_reports/config'

from flask import Flask, render_template
import cx_Oracle

app = Flask(__name__)
app.config.from_envvar('FLASK_ORACLE_CONFIG')

DSN = '''{0[USERNAME]}/{0[PASSWORD]}@ats'''.format(app.config)

def execute(conn, query):
    res = list()
    cur = conn.cursor()
    cur.execute(query)
    for data in cur.fetchall():
        res.append(list(data))
    cur.close()
    return res

def test():
    conn = cx_Oracle.connect(DSN)
    results = execute(conn, 'select platform_name from v$database')
    conn.close()
    return str(results)

@app.route('/')
def index():
    return render_template('index.html',
                           data=['engineer_list'])

@app.route('/engineer_list')
def engineer_list():
    conn = cx_Oracle.connect(DSN)
    results = execute(conn, 'select engineer_no, engineer_name from fisdata.engineers order by engineer_name')
    conn.close()
    return render_template('engineer_list.html',
                           data=results)

if __name__ == '__main__':
    print(app.config)
    print(test())
