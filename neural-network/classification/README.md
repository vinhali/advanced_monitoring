## Classificação de picos de consumo:

Este projeto tem como objetivo prever picos de consumo de CPU baseado na relação entre as varíaveis das 60 primeiras ocorrências (1 hora) com os picos das próximas 60 ocorrências.

## Modelo de dados:

<img src="https://github.com/vinhali/advanced_monitoring/blob/master/neural-network/classification/img/model.png?raw=true"/>

## Saída:

    [INFO] Sample rate generated is:

    [[[70, 2.23606797749979], [66, 5.477225575051661], [71, 1.4142135623730951], [75, 4.58257569495584], [68, 0.0]], [[78, 5.196152422706632], [69, 2.0], [69, 2.0], [69, 2.0], [69, 2.0]]]

    [END]
    
 ## Explicação do modelamento:
 
     5 médias (taxa)
                      --->  No range de 12 ocorrências (taxa) ----> no bloco 60 ocorrências (janela)
     5 desvios padrão


