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
            query = conn.execute('''select username, password from \"USERS_DYNAMIC\" 
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

    @app.route("/getForecastMemory")
    @auth.login_required
    def getForecastMemory():
        try:
            query = conn.execute('''SELECT server,forecastmemory,levelerror,datecollect,dateforecast
                                FROM "FORECASTMEMORY"
                                ORDER BY datecollect''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getForecastCpu")
    @auth.login_required
    def getForecastCpu():
        try:
            query = conn.execute('''SELECT server,forecastcpu,levelerror,datecollect,dateforecast
                                FROM "FORECASTCPU"
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
            #conn.commit()
            
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
            #conn.commit()
            
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

    @app.route("/setForecastGrafana", methods=['GET', 'POST'])
    @auth.login_required
    def setForecastGrafana():
        try:

            hostname = request.json['hostname']
            typeAnalisys = request.json['typeAnalisys']
            tresholdAnalisys = request.json['tresholdAnalisys']
            lossup = request.json['lossup']
            levelError = request.json['levelError']

            conn.execute('''INSERT INTO "FORECASTGRAFANA"
            (hostname,typeAnalisys,tresholdAnalisys,lossup,levelError,dateinsert)
            VALUES ('{0}','{1}','{2}',to_timestamp({3}),{4},current_timestamp)'''.
            format(hostname,typeAnalisys,tresholdAnalisys,int(lossup)/1000,levelError))
            #conn.commit()
            
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

class requestWeb(Resource):

    @app.route("/getHostname")
    @auth.login_required
    def getHostname():
        try:
            query = conn.execute('''SELECT hostname FROM "CI" ORDER BY hostname ASC''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getCustomer")
    @auth.login_required
    def getCustomer():
        try:
            query = conn.execute('''SELECT customer FROM "CUSTOMER" ORDER BY customer ASC''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getCustcode")
    @auth.login_required
    def getCustcode():
        try:
            query = conn.execute('''SELECT customer_code FROM "CUSTOMER" ORDER BY customer_code ASC''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getPlaybook")
    @auth.login_required
    def getPlaybook():
        try:
            query = conn.execute('''SELECT name FROM "PLAYBOOK" ORDER BY name ASC''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getUsers")
    @auth.login_required
    def getUsers():
        try:
            query = conn.execute('''SELECT * FROM "USERS_DYNAMIC" ORDER BY username ASC''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getListCustomer")
    @auth.login_required
    def getListCustomer():
        try:
            query = conn.execute('''SELECT * FROM "CUSTOMER" ORDER BY customer ASC''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getCI")
    @auth.login_required
    def getCI():
        try:
            query = conn.execute('''select
            "CI".idci,"CI".customer,"CI".customer_code,ip,hostname,sla,impact,
            estimativemoney,downtime,felling,location,type,journey,
            user,number_thrist,application,topology,support
            from "CI"
            inner join "IMPACT"
            on "IMPACT".idci = "CI".idci
            inner join "RELATIONSHIP"
            on "RELATIONSHIP".idci = "CI".idci
            inner join "DESCRIPTION"
            on "DESCRIPTION".idci = "CI".idci''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/getAnsibleHistory")
    @auth.login_required
    def getAnsibleHistory():
        try:
            query = conn.execute('''SELECT * FROM "ANSIBLE_HISTORY" ORDER BY playbook ASC''')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return json.dumps(result, default=json_util.default)
        except Exception as e:
            print("[ALERT] Error caused by: {}".format(e))

    @app.route("/setCustomer", methods=['GET', 'POST'])
    @auth.login_required
    def setCustomer():
        try:

            customer_code = request.json['customer_code']
            customer = request.json['customer']
            segment = request.json['segment']
            cnpj = request.json['cnpj']
            socialreason = request.json['socialreason']
            contact = request.json['contact']
            telephone = request.json['telephone']
            adress = request.json['adress']

            conn.execute('''INSERT INTO "CUSTOMER" (customer_code,customer,segment,cnpj,
            socialreason,contact,telephone,adress,datecustomer)
            VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',current_timestamp)'''.format(
            customer_code,customer,segment,cnpj,socialreason,contact,telephone,adress))
            #conn.commit()
            
        except Exception as e:

            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

    @app.route("/setUser", methods=['GET', 'POST'])
    @auth.login_required
    def setUser():
        try:

            uname = request.json['uname']
            pwd = request.json['pwd']
            customer = request.json['customer']
            privileges = request.json['privileges']

            conn.execute('''INSERT INTO "USERS_DYNAMIC" (username,password,customer,privileges,datecreate)
            VALUES ('{0}','{1}','{2}','{3}',current_timestamp)'''.format(uname,pwd,customer,privileges))
            #conn.commit()
            
        except Exception as e:

            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

    @app.route("/setCI", methods=['GET', 'POST'])
    @auth.login_required
    def setCI():
        try:

            code_id = request.json['code_id']
            customer = request.json['customer']
            idci = request.json['idci']
            hostname = request.json['hostname']
            ip = request.json['ip']

            conn.execute('''INSERT INTO "CI" (customer_code,customer,idci,hostname,ip,dateci)
            VALUES ('{0}','{1}','{2}','{3}','{4}',current_timestamp)'''.format(code_id,customer,
            idci,hostname,ip))
            #conn.commit()
            
        except Exception as e:

            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

    @app.route("/setImpact", methods=['GET', 'POST'])
    @auth.login_required
    def setImpact():
        try:

            idci = request.json['idci']
            sla_id = request.json['sla_id']
            impact_id = request.json['impact_id']
            money_id = request.json['money_id']
            dowtime_id = request.json['dowtime_id']
            feeling = request.json['feeling']

            conn.execute('''INSERT INTO "IMPACT" (idci,sla,impact,estimativemoney,downtime,felling,dateimpact)
            VALUES ('{0}','{1}','{2}','{3}','{4}','{5}',current_timestamp)'''.format(idci,sla_id,impact_id,
            money_id,dowtime_id,feeling))
            #conn.commit()
            
        except Exception as e:

            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

    @app.route("/setRelationship", methods=['GET', 'POST'])
    @auth.login_required
    def setRelationship():
        try:

            idci = request.json['idci']
            sector = request.json['sector']
            location = request.json['location']
            typeci = request.json['typeci']
            journey_id = request.json['journey_id']
            user_id = request.json['user_id']
            numberthirst = request.json['numberthirst']

            conn.execute('''INSERT INTO "RELATIONSHIP" (idci,sector,location,type,journey,"user",
            number_thrist,daterelationship)
            VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}',current_timestamp)'''.format(idci,sector,
            location,typeci,journey_id,user_id,numberthirst))
            #conn.commit()
            
        except Exception as e:

            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

    @app.route("/setDescription", methods=['GET', 'POST'])
    @auth.login_required
    def setDescription():
        try:

            idci = request.json['idci']
            application_id = request.json['application_id']
            topology_id = request.json['topology_id']
            support_id = request.json['support_id']

            conn.execute('''INSERT INTO "DESCRIPTION" (idci,application,topology,support,datedescription)
            VALUES ('{0}','{1}','{2}','{3}',current_timestamp)'''.format(idci,application_id,
            topology_id,support_id))
            #conn.commit()
            
        except Exception as e:

            print("[ALERT] Error caused by: {}".format(e))

        return "[INFO] Data is inserted [OK]"

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
