# -*- coding: utf-8 -*-
import os
import sys
import json
import psycopg2
from random import randrange
from ansible import context
from ansible.cli import CLI
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.utils.vars import load_extra_vars
from ansible.utils.vars import load_options_vars
from ansible.vars.manager import VariableManager
from ansible.errors import AnsibleError, AnsibleParserError, AnsibleUndefinedVariable, AnsibleFileNotFound, AnsibleAssertionError, AnsibleTemplateError
from ansible.plugins.callback import CallbackBase

IDOPeration = randrange(10000000)
hosts_path = '/etc/ansible/hosts'
play_path = '/etc/ansible/playbooks/'

class ModuleResultsCollector():

    def connpg(self, query):
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

    def header(self, user, frequency, playbook, customer, host):
        print("******************************************************************")
        print('''Starting with config:
        User: {0}
        Frequency: {1}
        Playbook: {2}
        Customer: {3}
        Host: {4}'''.format(user,frequency,playbook,customer,host))
        print("******************************************************************")
        flow = ModuleResultsCollector()
        flow.running(IDOPeration, user, frequency, playbook, customer, host)

    def passed(self, IDOPeration, affected_host, namePlay, status):

        print("Passed       *****************************************************")

        try:
            flow = ModuleResultsCollector()
            flow.connpg("UPDATE \"ANSIBLE_HISTORY\" SET status = '{1}' WHERE idoPeration = '{0}'"\
            .format(IDOPeration, status))

            try:

                os.system('''php /etc/ansible/open_tickets/open.php eventhost="{}" event="OPEN" state="PASSED" hostproblemid=0 lasthostproblemid=0 servico="{}" triggerid="{}" eventansible="Dynamic - AUTO RESOLVED"'''
                .format(affected_host,namePlay,IDOPeration))

                print("Created ticket [ok]")
                

            except Exception as e:

                print("[INFO] Failed open ticket - Caused by: {}".format(e))

        except:

            print("Failed commit --> Status = PASSED ********************************")

        finally:

            print("End script   *****************************************************")
            print("******************************************************************")

    def failed(self, IDOPeration, affected_host, namePlay, status):

        print("Failed start *****************************************************")

        try:

            flow = ModuleResultsCollector()
            flow.connpg("UPDATE \"ANSIBLE_HISTORY\" SET status = '{1}' WHERE idoPeration = '{0}'"\
            .format(IDOPeration, status))

        except:

            print("Failed commit --> Status = FAILED ********************************")

        try:

            os.system('''php /etc/ansible/open_tickets/open.php eventhost="{}" event="OPEN" state="FAILED" hostproblemid=0 lasthostproblemid=0 servico="{}" triggerid="{}" eventansible="Dynamic - AUTO RESOLVED"'''
            .format(affected_host,namePlay,IDOPeration))
            
            print("Created ticket for failed in playbook [ok]")
            

        except Exception as e:

            print("[INFO] Failed open ticket - Caused by: {}".format(e))

        finally:

            print("End script   *****************************************************")
            print("******************************************************************")

    def running(self, IDOPeration, user, frequency, playbook, customer, host):

        print("Start play   *****************************************************")

        try:

            flow = ModuleResultsCollector()
            flow.connpg('''INSERT INTO \"ANSIBLE_HISTORY\"
            (idoPeration, playbook,technican,status,frequency,customer,host,startdate)
            VALUES ('{0}', '{3}','{1}','RUNNING','{2}','{4}','{5}',current_timestamp)'''
            .format(IDOPeration, user,frequency,playbook,customer,host))

            print("Started      *****************************************************")

            flow.run_playbook(host, hosts_path, play_path+playbook, playbook, user)

        except:

            flow = ModuleResultsCollector()
            flow.failed(IDOPeration, host,playbook, 'FAILED')

    def run_playbook(self, affected_host, host_file, playbook_path, namePlay, selectuser):

        if not os.path.exists(playbook_path):
            print('[INFO] The playbook does not exist: "{0}"'.format(playbook_path))
            sys.exit()

        if not os.path.isfile(host_file):
            print('[INFO] Host file does not exist: "{0}"'.format(host_file))
            sys.exit()

        try:

            loader = DataLoader()
            passwords = dict(vault_pass='pass')

            context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                                module_path=None, forks=100, remote_user=selectuser, private_key_file=None, extra_vars=[{'affected_hosts':''+affected_host+''}],
                                ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
                                become_method='sudo', become_user=selectuser, verbosity=True, check=False, start_at_task=None)

            inventory = InventoryManager(loader=loader, sources=(host_file))

            variable_manager = VariableManager(loader=loader, inventory=inventory, version_info=CLI.version_info(gitinfo=False))

            pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, passwords=passwords)

            try:

                execPlay = json.dumps({affected_host: pbex.run()}, indent=4)
                check = json.loads(execPlay)

                if(check[affected_host] == 2):

                    flow = ModuleResultsCollector()
                    flow.failed(IDOPeration, affected_host, namePlay, 'FAILED')
                    print('[INFO] Playbook failed: {}'.format(playbook_path))

                elif (check[affected_host] == 4):
                    
                    flow = ModuleResultsCollector()
                    flow.failed(IDOPeration, affected_host, namePlay, 'FAILED')
                    print('[INFO] Playbook unreachable: {}'.format(playbook_path))

                else:

                    flow = ModuleResultsCollector()
                    flow.passed(IDOPeration, affected_host, namePlay, 'PASSED')
                    print('[INFO] Playbook pass: {} [ok]'.format(playbook_path))

            except AnsibleError as ansError:

                flow = ModuleResultsCollector()
                flow.failed(IDOPeration, affected_host, namePlay, 'FAILED')
                print('[INFO] Ansible error: {}'.format(ansError))

        except Exception as e:

            flow = ModuleResultsCollector()
            flow.failed(IDOPeration, affected_host, namePlay, 'FAILED')
            print('[INFO]: {} - Failed caused by: {}'.format(playbook_path,e))

if __name__ == "__main__":
    
    flow = ModuleResultsCollector()
    flow.header(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
