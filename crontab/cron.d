#Collect memory in API ZABBIX
* * 1 * * /usr/bin/python3.7 /etc/neural/getValues.py "http://192.168.1.135/zabbix" "Admin" "zabbix" "Servers Production" "Memória em uso (Porcentagem)" 90 "127.0.0.1" "networkneural" "postgres" "postgres" "MEMORYEXPORTZB" >> /etc/neural/logs/collectMemory.log >> /etc/neural/logs/collectMemory.log

#Collect CPU in API Zabbix
* * 1 * * /usr/bin/python3.7 /etc/neural/getValues.py "http://192.168.1.135/zabbix" "Admin" "zabbix" "Servers Production" "Uso do processador na média de 1 minuto" 90 "127.0.0.1" "networkneural" "postgres" "postgres" "CPUEXPORTZB" >> /etc/neural/scripts/logs/collectCpu.log

#Analisys neural for Memory
* * 1 * * /usr/bin/python3.7 /etc/neural/ConsumptionAnalysisNeuralNetworkMemory.py >> /etc/neural/logs/neuralMemory.log

#Analisys neural for CPU
* * 1 * * /usr/bin/python3.7 /etc/neural/ConsumptionAnalysisNeuralNetworkCpu.py >> /etc/neural/logs/neuralCpu.log
