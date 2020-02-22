## :rocket: PostgreSQL

Modelo do banco de dados


## Hierarquia

    PostgreSQL
        └── Zabbix
             └── Data Set
                  └── Data Result
                       └── Glpi
## Liberar conexão remota no postgresql

    1. Modify two configure files
    # vi /var/lib/pgsql/data/postgresql.conf
     Replace the line:
    listen_addresses = 'localhost'  -> listen_addresses = '*'
    # vi /var/lib/pgsql/data/pg_hba.conf
     Add the line at the very end:
    host all all 0.0.0.0/0 trust
    (If IPv6:
    host all all ::/0 trust) 
    2. Restart the database service
    # service postgresql restart
    3. Disable the firewall
    # rcSuSEfirewall2 stop
    # chkconfig SuSEfirewall2 off
    # chkconfig SuSEfirewall2_init off
