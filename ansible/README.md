## :rocket: Ansible

Playbook para START da VM

## Hierarquia

    Zabbix
        └── Treshold >= Definido
             └── API-ZABBIX
                  └── Redes Neurais Recorrentes
                       └── Health Check Script
                             └── Ansible

## Estrutura

    playbooks
    |   └── roles
    |        └── troubleshooting
    |            └── tasks
    |                 └── startVM.yml
    |
    group_vars
     └── all.yml
         
