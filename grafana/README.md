## :rocket: Grafana

JSON do dashboard

## Hierarquia

    Zabbix
        └── Treshold >= Definido
             └── API-ZABBIX
                  └── Redes Neurais Recorrentes
                       └── Health Check Script
                             └── Ansible
                                  └── GLPI - Ticket
                                        └── Grafana - Dashboard

## Redirecionar porta

sudo setcap 'cap_net_bind_service=+ep' /usr/sbin/grafana-server 
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3000

## Liberar acesso no frame

vim /etc/grafana/grafana.ini

cookie_secure = true
cookie_smesite =true
allow_embedding = true

