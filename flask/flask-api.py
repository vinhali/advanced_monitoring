from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from bson import json_util
import json
import psycopg2
from flask import Flask
from flask import current_app
from flask_httpauth import HTTPBasicAuth

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
            query = conn.execute("select * from \"MEMORYEXPORTZB\"")
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getCpu")
    @auth.login_required
    def getCpu():
        try:
            query = conn.execute("select * from \"CPUEXPORTZB\"")
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getDisk")
    @auth.login_required
    def getDisk():
        try:
            query = conn.execute("select * from \"DISKEXPORTZB\"")
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
