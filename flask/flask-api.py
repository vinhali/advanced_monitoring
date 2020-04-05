try:
    from flask import Flask, request, jsonify
    from flask_restful import Resource, Api
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import scoped_session, sessionmaker
    from bson import json_util
    from datetime import datetime
    from flask import Flask, session
    from flask import current_app
    from flask_httpauth import HTTPBasicAuth
    from json import dumps
    import json
    import psycopg2
    import sys
except ImportError as e:
    print("[ALERT] Error import caused by: {}".format(e))
    sys.exit()

try:
    db_connect = create_engine('postgresql+psycopg2://postgres:postgres@localhost/networkneural')
    conn = db_connect.connect()
except Exception as e:
    print("[ALERT] Error caused by: {}".format(e))

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
            query = conn.execute('''SELECT hostname,itemid,itemname,itemkey,
                                    historyvalue,datecollect,dateinsert
                                    FROM "MEMORYEXPORTZB"
                                    ORDER BY datecollect''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getCpu")
    @auth.login_required
    def getCpu():
        try:
            query = conn.execute('''SELECT hostname,itemid,itemname,itemkey,
                                    historyvalue,datecollect,dateinsert
                                    FROM "CPUEXPORTZB" ORDER BY datecollect''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getDisk")
    @auth.login_required
    def getDisk():
        try:
            query = conn.execute('''SELECT hostname,itemid,itemname,itemkey,
                                historyvalue,datecollect,dateinsert
                                FROM "DISKEXPORTZB"
                                ORDER BY datecollect''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

class ApiNeural(Resource):
    @app.route("/setForecastMemory", methods=['GET', 'POST'])
    @auth.login_required
    def setForecastMemory():
        try:

            server = request.json['server']
            forecastmemory = request.json['forecastmemory']
            levelerror = request.json['levelerror']
            datecollect = request.json['datecollect']

            conn.execute('''INSERT INTO "FORECASTMEMORY"
            (server,forecastmemory,levelerror,datecollect,dateforecast)
            VALUES ('{0}','{1}','{2}',to_timestamp({3}) AT TIME ZONE 'UTC',current_timestamp)'''.
            format(server,forecastmemory,levelerror,int(datecollect)/1000))
            
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

    @app.route("/setForecastCpu", methods=['GET', 'POST'])
    @auth.login_required
    def setForecastCpu():
        try:

            server = request.json['server']
            forecastcpu = request.json['forecastcpu']
            levelerror = request.json['levelerror']
            datecollect = request.json['datecollect']

            conn.execute('''INSERT INTO "FORECASTCPU"
            (server,forecastcpu,levelerror,datecollect,dateforecast)
            VALUES ('{0}','{1}','{2}',to_timestamp({3}) AT TIME ZONE 'UTC',current_timestamp)'''.
            format(server,forecastcpu,levelerror,int(datecollect)/1000))
            
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

    @app.route("/setForecastDisk", methods=['GET', 'POST'])
    @auth.login_required
    def setForecastDisk():
        try:

            server = request.json['server']
            forecastdisk = request.json['forecastdisk']
            levelerror = request.json['levelerror']
            datecollect = request.json['datecollect'].replace('000','')

            conn.execute('''INSERT INTO "FORECASTDISK"
            (server,forecastdisk,levelerror,datecollect,dateforecast)
            VALUES ('{0}','{1}','{2}',to_timestamp({3}) AT TIME ZONE 'UTC',current_timestamp)'''.
            format(server,forecastdisk,levelerror,int(datecollect)/1000))
            
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
