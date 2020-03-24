# -*- coding: utf-8 -*-
import os
import sys
import json
from ansible import context
from ansible.cli import CLI
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.errors import AnsibleError, AnsibleParserError, AnsibleUndefinedVariable, AnsibleFileNotFound, AnsibleAssertionError, AnsibleTemplateError
from ansible.plugins.callback import CallbackBase

class ModuleResultsCollector():

    def run_playbook(self, affected_host, host_file, playbook_path, selectuser, selectpass, extra_vars=None):

        if not os.path.exists(playbook_path):
            print('[INFO] The playbook does not exist: "{0}"'.format(playbook_path))
            sys.exit()

        elif not os.path.isfile(host_file):
            print('[INFO] Host file does not exist: "{0}"'.format(host_file))

        else:

            try:

                loader = DataLoader()
                passwords = dict(vault_pass=selectpass)

                context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                                    module_path=None, forks=100, remote_user=selectuser, private_key_file=None,
                                    ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
                                    become_method='sudo', become_user=selectuser, verbosity=True, check=False, start_at_task=None)

                inventory = InventoryManager(loader=loader, sources=(host_file))

                variable_manager = VariableManager(loader=loader, inventory=inventory, version_info=CLI.version_info(gitinfo=False))

                #variable_manager.extra_vars = {'affected_hosts': 'webserver'}

                pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, passwords=passwords)

                try:

                    execPlay = json.dumps({affected_host: pbex.run()}, indent=4)
                    check = json.loads(execPlay)

                    if(check[affected_host] == 2):
    
                        print('[INFO] Playbook failed: {}'.format(playbook_path))

                    elif (check[affected_host] == 4):
                        
                        print('[INFO] Playbook unreachable: {}'.format(playbook_path))

                    else:

                        print('[INFO] Playbook pass: {} [ok]'.format(playbook_path))

                except AnsibleError as ansError:

                    print('[INFO] Ansible error: {}'.format(ansError))

            except Exception as e:

                print('[INFO]: {} - Failed caused by: {}'.format(playbook_path,e))

selectuser = 'root'
selectpass = 'root'
selectplay = 'GEN_CLEAN_MEMORY_LINUX.yml'
host_file = '/etc/ansible/hosts'
affected_host = 'hostname-here'

flow = ModuleResultsCollector()
flow.run_playbook(affected_host, host_file, '/etc/ansible/playbooks/'+selectplay+'', selectuser, selectpass)
