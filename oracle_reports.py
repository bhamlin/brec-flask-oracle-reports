#!/usr/bin/python3

import os
import sys

os.environ['ORACLE_HOME'] = '/usr/lib/oracle/11.2/client64'
os.environ['TNS_ADMIN'] = '/usr/lib/oracle/11.2/client64'
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'

os.environ['FLASK_ORACLE_CONFIG'] = '/etc/flask_oracle_reports/config'

from flask import Flask, Response, render_template
import cx_Oracle

app = Flask(__name__)
app.config.from_envvar('FLASK_ORACLE_CONFIG')

DSN = '''{0[USERNAME]}/{0[PASSWORD]}@ats'''.format(app.config)

import reports

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
                           title='Report list',
                           data=reports.available )

@app.route('/report/<string:report_name>')
def show_report(report_name):
    if report_name in reports.available:
        report = reports.available[report_name]
        conn = cx_Oracle.connect(DSN)
        results = execute(conn, report.query)
        conn.close()
        return render_template(report.template,
                               report_name=report_name,
                               title=report.title,
                               data=results)

@app.route('/csv/<string:report_name>.csv')
def show_csv(report_name):
    if report_name in reports.available:
        report = reports.available[report_name]
        conn = cx_Oracle.connect(DSN)
        try:
            results = execute(conn, report.query)
        except cx_Oracle.DatabaseError as exc:
            app.logger.error(exc)
        conn.close()
        return Response(report.to_csv(results),
                        headers={
                            'Content-Type': 'text/csv',
                            'Content-Disposition': 'attachment; filename={}.csv'.format(report_name)
                        })
        
if __name__ == '__main__':
    print(app.config)
    print(test())
