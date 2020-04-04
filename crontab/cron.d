#Collect Memory in API ZABBIX
* * 1 * * /usr/bin/python3.7 /etc/neural/getValues.py "http://192.168.1.135/zabbix" "Admin" "zabbix" "Servers Production" "Memória em uso (Porcentagem)" 90 "127.0.0.1" "networkneural" "postgres" "postgres" "MEMORYEXPORTZB" >> /etc/neural/logs/collectMemory.log

#Collect CPU in API Zabbix
* * 1 * * /usr/bin/python3.7 /etc/neural/getValues.py "http://192.168.1.135/zabbix" "Admin" "zabbix" "Servers Production" "Uso do processador na média de 1 minuto" 90 "127.0.0.1" "networkneural" "postgres" "postgres" "CPUEXPORTZB" >> /etc/neural/logs/collectCpu.log

# Collect Disk in API
* * 1 * * /usr/bin/python3.7 /etc/neural/getValues.py "http://192.168.1.135/zabbix" "Admin" "zabbix" "Servers Production" "Disco total Free (%)" 90 "127.0.0.1" "networkneural" "postgres" "postgres" "DISKEXPORTZB" >> /etc/neural/logs/collectDisk.log

#Analisys neural for Memory
* * 1 * * /usr/bin/python3.7 /etc/neural/ConsumptionAnalysisNeuralNetworkMemory.py >> /etc/neural/logs/neuralMemory.log

#Analisys neural for CPU
* * 1 * * /usr/bin/python3.7 /etc/neural/ConsumptionAnalysisNeuralNetworkCpu.py >> /etc/neural/logs/neuralCpu.log

#Analisys neural for Disk
* * 1 * * /usr/bin/python3.7 /etc/neural/ConsumptionAnalysisNeuralNetworkDisk.py >> /etc/neural/logs/neuralDisk.log
