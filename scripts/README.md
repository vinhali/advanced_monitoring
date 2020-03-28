## :rocket: Scripts em python

- <a href="https://pypi.org/project/py-zabbix/">API Zabbix</a>
- Nome do grupo API: Servers Production
- Health Check


## Hierarquia

    Zabbix
        └── Treshold >= Definido
             └── API-ZABBIX
                  └── Redes Neurais Recorrentes
                       └── Health Check Script

## Example command [range=90days]

    python3 /etc/neural/scripts/getValues.py "http://192.168.1.135/zabbix" "Admin" "zabbix" "Servers Production" "Memória em uso (Porcentagem)" 90 "127.0.0.1" "networkneural" "postgres" "postgres" "MEMORYEXPORTZB"

## Example crontab

    * * 1 * * /usr/bin/python3.7 /etc/neural/scripts/getValues.py "http://192.168.1.135/zabbix" "Admin" "zabbix" "Servers Production" "Memória em uso (Porcentagem)" 90 "127.0.0.1" "networkneural" "postgres" "postgres" "MEMORYEXPORTZB" >> /etc/neural/scripts/logs/collectMemory.log
