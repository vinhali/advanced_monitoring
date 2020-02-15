#!/usr/bin/env python
import psycopg2
from datetime import datetime
import sys
from ansible import context
from ansible.cli import CLI
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager

# Connection with postgres
connpostgres = psycopg2.connect("host='127.0.0.1'"
                        " dbname='networkneural'"
                        " user='postgres'"
						" password=postgres")
cursorpost = connpostgres.cursor()

cursorpost.execute('SELECT forecastvalue, datecollect, hostname FROM forecastmemoryconsumption WHERE forecastvalue::numeric::int >= 85 LIMIT 1')
treshold = cursorpost.fetchone()

format = '%Y-%m-%d %H:%M:%S'
hourLimit = datetime.strptime(treshold[1], format)

import datetime
now = datetime.datetime.now()

if treshold[0] != None:

	if now.hour == now.hour and now.minute == now.minute:
	#if now.hour == hourLimit.hour and now.minute == hourLimit.minute:

		loader = DataLoader()
		passwords = dict(vault_pass='ellen')

		context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
		                    module_path=None, forks=100, remote_user='luisvinhali', private_key_file=None,
		                    ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
		                    become_method='sudo', become_user='luisvinhali', verbosity=True, check=False, start_at_task=None)

		inventory = InventoryManager(loader=loader, sources=('/home/userinfra/detector/hosts',))

		variable_manager = VariableManager(loader=loader, inventory=inventory, version_info=CLI.version_info(gitinfo=False))

		pbex = PlaybookExecutor(playbooks=['/home/userinfra/detector/startvm.yml'], inventory=inventory, variable_manager=variable_manager, loader=loader, passwords=passwords)

		results = pbex.run()

	else:
		print ('its not the time for eating lunch')
else:
	print('error api-ansible')


# ansible servidores -i hosts -u luisvinhali -k -a "VBoxManage startvm 'CLIENT2:SRV:LZ:DATA2' --type headless"


