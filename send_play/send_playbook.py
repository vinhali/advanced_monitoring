import sys
from datetime import datetime
import sys
import paramiko

class ModuleResultsCollector():

    def header(self, user, frequency, playbook, customer, host):
        print("******************************************************************")
        print('''Send with config:
        User: {0}
        Frequency: {1}
        Playbook: {2}
        Customer: {3}
        Host: {4}'''.format(user,frequency,playbook,customer,host))
        print("******************************************************************")
        flow = ModuleResultsCollector()
        flow.startplaybook(user, frequency, playbook, customer, host)

    def startplaybook(self, user, frequency, playbook, customer, host):
            
        try:

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect('192.168.1.139', username='root', password='root') # use shared key - best pratcies

            stdin, stdout, stderr = client.exec_command('python /etc/ansible/scripts/activePlay.py {0} {1} {2} {3} {4}'.format(user, frequency, playbook, customer, host), get_pty=True)

            for line in iter(lambda: stdout.readline(2048), ""): 
                print(line, end="")

        except Exception as e:

            print('Failed caused by: {}', e)

if __name__ == "__main__":
    
    flow = ModuleResultsCollector()
    flow.header(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
