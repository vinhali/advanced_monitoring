from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from bson import json_util
import json
from json import dumps
import psycopg2
from flask import Flask
from flask import current_app
from flask_httpauth import HTTPBasicAuth
import sys

db_connect = create_engine('postgresql+psycopg2://postgres:postgres@localhost/networkneural')
conn = db_connect.connect()
app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

class Credentials(Resource):
    @auth.verify_password
    def verify_password(username, password):
        try:
            query = conn.execute('''select username, password from \"USERS_ANSIBLE\" 
            WHERE username = '{}' and password = '{}'; '''.format(username, password))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            resultDumps =  json.dumps(result[0], default=json_util.default)
            indentify =  json.loads(resultDumps)
            if indentify['username'] == username and indentify['password'] == password:
                return True
            else:
                return False
        except:
            return False

class ApiZabbix(Resource):
    @app.route("/getMemory")
    @auth.login_required
    def getMemory():
        try:
            query = conn.execute('''SELECT DISTINCT ON (date_trunc('minute', datecollect))
            hostname,itemid,itemname,itemkey,historyvalue,datecollect,dateinsert
            FROM "MEMORYEXPORTZB"
            WHERE date_trunc('day', datecollect) = '2020-02-25'
            ORDER BY date_trunc('minute', datecollect)''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getCpu")
    @auth.login_required
    def getCpu():
        try:
            query = conn.execute('''SELECT DISTINCT ON (date_trunc('minute', datecollect))
            hostname,itemid,itemname,itemkey,historyvalue,to_char(datecollect, 'yyyy-mm-dd hh:mm:ss'),dateinsert
            FROM "CPUEXPORTZB"
            WHERE date_trunc('day', datecollect) = '2020-02-25'
            ORDER BY date_trunc('minute', datecollect)''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getDisk")
    @auth.login_required
    def getDisk():
        try:
            query = conn.execute('''SELECT DISTINCT ON (date_trunc('minute', datecollect))
            hostname,itemid,itemname,itemkey,historyvalue,to_char(datecollect, 'yyyy-mm-dd hh:mm:ss'),dateinsert
            FROM "DISKEXPORTZB"
            WHERE date_trunc('day', datecollect) = '2020-02-25'
            ORDER BY date_trunc('minute', datecollect)''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

class ApiNeural(Resource):
    @app.route("/setForecast", methods=['GET', 'POST'])
    @auth.login_required
    def setForecast():
        try:

            idci = request.json['idci']
            forecastmemory = request.json['forecastmemory']
            forecastcpu = request.json['forecastcpu']
            forecastcapacity = request.json['forecastcapacity']
            forecastuptime = request.json['forecastuptime']
            levelerror = request.json['levelerror']
            datecollect = request.json['datecollect']
            dateforecast = request.json['dateforecast']

            conn.execute('''INSERT INTO "FORECAST"
            (idci,forecastmemory,forecastcpu,forecastcapacity,
            forecastuptime,levelerror,datecollect,dateforecast)
            VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')'''.format(
            idci,forecastmemory,forecastcpu,forecastcapacity,forecastuptime,levelerror,
            datecollect,dateforecast))
            conn.commit()
            
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
