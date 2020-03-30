from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from bson import json_util
import json
import psycopg2
from flask import Flask

db_connect = create_engine('postgresql+psycopg2://postgres:postgres@localhost/networkneural')
app = Flask(__name__)
api = Api(app)

class ApiZabbix(Resource):
    @app.route("/getMemory")
    def getMemory():
        try:
            conn = db_connect.connect()
            query = conn.execute("select * from \"MEMORYEXPORTZB\"")
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getCpu")
    def getCpu():
        try:
            conn = db_connect.connect()
            query = conn.execute("select * from \"CPUEXPORTZB\"")
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getDisk")
    def getDisk():
        try:
            conn = db_connect.connect()
            query = conn.execute("select * from \"DISKEXPORTZB\"")
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
