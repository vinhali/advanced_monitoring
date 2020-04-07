## :rocket: Redes Neurais Recorrentes

Scripts em python


## Hierarquia

    Zabbix
        └── Treshold >= Definido
             └── API-ZABBIX
                  └── Redes Neurais Recorrentes

## Para retornar o valor como único na previsão dentro da série temporal, modifique para:

    periods = 1
    future_forecast = 1

    X = base[0:(len(base) - (len(base) % periods))]
    X_batches = X.reshape(-1, periods, 1)

    y = base[0:(len(base) - (len(base) % periods)) + future_forecast]
    y_batches = y.reshape(-1, periodos, 1)
