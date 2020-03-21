import sys
import psycopg2
from datetime import datetime
import sys
import paramiko
from random import randrange

IDOPeration = randrange(10000000)

def connpg(query):
    # Connection with postgres
	connpostgres = psycopg2.connect("host='192.168.1.138'"
							" dbname='networkneural'"
							" user='postgres'"
							" password='postgres'")
	cursorpost = connpostgres.cursor()
	cursorpost.execute(query)
	connpostgres.commit()
	cursorpost.close
	connpostgres.close()

def header(user, frequency, playbook, customer, host):
	print("******************************************************************")
	print('''Starting with config:
	User: {0}
	Frequency: {1}
	Playbook: {2}
	Customer: {3}
	Host: {4}'''.format(user,frequency,playbook,customer,host))
	print("******************************************************************")
	running(IDOPeration, user, frequency, playbook, customer, host)

def passed(IDOPeration, status):

	print("Passed       *****************************************************")

	try:

		connpg("UPDATE \"ANSIBLE_HISTORY\" SET status = '{1}' WHERE idoPeration = '{0}'"\
		.format(IDOPeration, status))

	except:

		print("Failed commit --> Status = PASSED ********************************")

	finally:

		print("End script   *****************************************************")
		print("******************************************************************")

def failed(IDOPeration, status):

	print("Failed start *****************************************************")

	try:

		connpg("UPDATE \"ANSIBLE_HISTORY\" SET status = '{1}' WHERE idoPeration = '{0}'"\
		.format(IDOPeration, status))

	except:

		print("Failed commit --> Status = FAILED ********************************")

	finally:

		print("End script   *****************************************************")
		print("******************************************************************")

def running(IDOPeration, user, frequency, playbook, customer, host):

	print("Start play   *****************************************************")

	try:

		connpg('''INSERT INTO \"ANSIBLE_HISTORY\"
		(idoPeration, playbook,technican,status,frequency,customer,host,startdate)
		VALUES ('{0}', '{3}','{1}','RUNNING','{2}','{4}','{5}',current_timestamp)'''
		.format(IDOPeration, user,frequency,playbook,customer,host))
		print("Started      *****************************************************")

		startplaybook(playbook,user,host)

	except:

		failed(IDOPeration, 'FAILED')

def startplaybook(name,user,iventory):
    	
	try:

		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect('192.168.1.139', username='root', password='root')

		stdin, stdout, stderr = client.exec_command('ansible-playbook /etc/ansible/playbooks/'+name+' --extra-vars "host='+iventory+', user='+user+'"', get_pty=True)

		for line in iter(lambda: stdout.readline(2048), ""): 
			print(line, end="")

		client.close()

		passed(IDOPeration, 'PASSED')

	except:

		failed(IDOPeration, 'FAILED')

if __name__ == "__main__":
    	
    header(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
